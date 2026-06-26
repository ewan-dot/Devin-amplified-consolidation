---
artifact: beast-tailscale-recovery-plan
created_utc: 2026-06-25T12:52:00Z
origin: perplexity
author: perplexity-computer
for: ewan + on-Mac AI partners (M5/M4)
status: ready-to-execute
tier: STRUCTURED  # research-derived, not yet measured against this specific box
type: ops-runbook
goal: get the Beast (Hetzner dedicated) back online and rejoin tailnet
---

# Beast + Tailscale recovery — runbook

## TL;DR — what is almost certainly going on

You activated Hetzner **rescue mode**, then reset. Two failure modes match the symptoms; both are common and well-documented.

1. **The box is still booted into rescue** (the in-RAM Hetzner mini-Linux), not your installed OS. Rescue does not run your `tailscaled`, your services, or your network config — so M5/M4 cannot reach the Beast over Tailscale by definition. Rescue is one-shot and auto-disables on first boot or after 60 min idle ([Hetzner Cloud API — Disable Rescue](https://306b3e51cy.apidog.io/api-3536571)), but on **Robot dedicated** the box only leaves rescue once you actually reboot from rescue back into the installed OS.
2. **Tailscale node key expired / state stale** on this machine. After long downtime or a reinstall, the node shows greyed-out in the admin console and clients cannot reach it until you reauth with `tailscale up --force-reauth` ([Tailscale issue #367](https://github.com/tailscale/tailscale/issues/367), [issue #9382 — machine identity in `tailscaled.state`](https://github.com/tailscale/tailscale/issues/9382), [OPNsense forum confirmation](https://forum.opnsense.org/index.php?topic=45260.0)).

Order of operations: **fix boot first, fix Tailscale second**. Don't touch Tailscale until the installed OS is actually running.

---

## Phase 1 — Confirm what the box is actually booted into

From any machine that can reach the Beast's **public IPv4** (not via Tailscale — bypass Tailscale entirely for this phase):

```bash
# Replace <BEAST_PUBLIC_IP> with the Hetzner-assigned public IP from Robot.
ssh -o StrictHostKeyChecking=accept-new root@<BEAST_PUBLIC_IP>
```

Then inside the session, run:

```bash
# Is this rescue, or the installed OS?
uname -a
cat /etc/hostname
cat /etc/os-release
# Rescue gives itself away: hostname is usually "rescue" and / is a tmpfs/ramdisk
mount | grep " / "
df -h /
# Look for the marker file rescue leaves behind
ls -la /etc/H* 2>/dev/null    # /etc/Hetzner exists in rescue
ls /root/.oldroot 2>/dev/null
```

Interpretation:

- `hostname == rescue` **or** root mounted on `tmpfs`/`overlay` → **still in rescue**. Go to Phase 2A.
- Hostname is your normal one, real disk mounted on `/` → **installed OS booted**. Skip to Phase 3.
- SSH refuses / times out on public IP → Phase 2B.

> If you don't know the public IP off the top of your head, it's on the server's overview page in Hetzner Robot, and also in any old `~/.ssh/known_hosts` entry on M5/M4: `grep -i hetzner ~/.ssh/known_hosts` or scan known IPs.

---

## Phase 2A — Box is still in rescue: boot the installed OS

Rescue auto-disables on the **next** clean reboot, but if you've been thrashing resets it may keep landing back in rescue. Do this:

1. In **Hetzner Robot** → the server → **Rescue** tab → confirm rescue is **deactivated** (no active rescue session shown). If it's still active, click **Deactivate**.
2. From the rescue shell, do a clean shutdown-reboot rather than a hard reset:

```bash
# from inside the rescue ssh session
sync
shutdown -r now
```

3. Wait ~3–5 minutes. Re-SSH on the public IP. Re-run the Phase 1 detection. If you're now on the installed OS → Phase 3.
4. If it still boots into rescue: in Robot, do **Reset** → choose **Send CTRL+ALT+DEL** or **Press power button (short)**, not "Activate hardware reset" with rescue armed. The "Execute an automatic hardware reset" button only does what you tell it; the boot target is governed by the Rescue tab state.
5. If it **still** lands in rescue, the installed-OS bootloader is broken. Symptoms: BIOS POSTs but no GRUB / kernel panic / `mdadm` array degraded. This is a separate, more serious recovery — see Appendix A.

---

## Phase 2B — Can't even SSH on the public IP

1. In Robot, open the **KVM console** (request one if not provisioned — Hetzner usually gives a few hours free on dedicated). This shows the actual screen.
2. If you see a GRUB prompt, kernel panic, `emergency mode`, or `(initramfs)` — that's a boot-time failure, not a network failure. See Appendix A.
3. If the box looks fully up at a login prompt but SSH is refused, it's either:
   - `sshd` not started → log in on console, `systemctl status sshd`, `systemctl start sshd`.
   - Firewall rule from a previous Tailscale-only lockdown. Check `iptables -L -n` / `nft list ruleset` / `ufw status`. If you'd previously hardened SSH to Tailscale-only (very common pattern), the box has locked you out of its own public IP — temporarily open port 22 from console: `ufw allow 22/tcp` or `iptables -I INPUT -p tcp --dport 22 -j ACCEPT`.

---

## Phase 3 — Installed OS is up. Now fix Tailscale.

You are SSH'd into the real Beast on its public IP. Run these in order; stop at the first one that succeeds.

```bash
# 3.1 — Is tailscaled even running?
systemctl status tailscaled
journalctl -u tailscaled -n 100 --no-pager

# 3.2 — If inactive/failed, just start it:
systemctl enable --now tailscaled

# 3.3 — Check current Tailscale state from the daemon's POV
tailscale status
# Look for: "NeedsLogin", "expired", "stopped", or an empty peer list.
```

### Decision tree on `tailscale status` output

- **"Logged out" / "NeedsLogin"** → the auth/node key is gone or expired:

  ```bash
  tailscale up --ssh --accept-routes --force-reauth
  ```

  This will print a one-time URL. Open it on M5, sign in, approve the machine. ([Tailscale KB on key expiry](https://tailscale.com/kb/1028/key-expiry/))

- **Daemon reports node is there but peers can't see it** → node is shown greyed-out in the Tailscale admin console. Fix:

  1. Open [https://login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines) on M5.
  2. Find the Beast row. If it shows "Expired", click the three-dot menu → **Disable key expiry** (do this for servers; only do this for machines you trust — the Beast qualifies) ([Tailscale KB 1028](https://tailscale.com/kb/1028/key-expiry/)).
  3. Then click "Reauthenticate" or run `tailscale up --force-reauth` on the Beast.

- **`failed to connect to local tailscaled`** even though `systemctl status` says active → state file corruption (seen in [CSDN report](https://blog.csdn.net/weixin_44212848/article/details/144086815)):

  ```bash
  tailscale down
  systemctl stop tailscaled
  mv /var/lib/tailscale/tailscaled.state /var/lib/tailscale/tailscaled.state.bak-$(date -u +%Y%m%dT%H%M%SZ)
  systemctl start tailscaled
  tailscale up --ssh --accept-routes
  ```

  Note from [issue #9382](https://github.com/tailscale/tailscale/issues/9382): moving `tailscaled.state` changes the machine identity, so the node will reappear in the admin console as a **new** machine. Remove the old greyed-out one to keep the list clean.

- **`tailscale up` hangs forever with no login URL** → check for a conflicting VPN / firewall mark (the Mullvad+Tailscale failure mode in [dev.to writeup](https://dev.to/yulieff/how-to-run-tailscale-and-mullvad-together-on-manjaro-linux-25ke)). On a Hetzner server this is more likely an outbound firewall blocking UDP 41641 or DERP (443/TCP) — confirm:

  ```bash
  # Outbound to DERP relays should work
  curl -v https://controlplane.tailscale.com 2>&1 | head -20
  # If this fails, your egress is broken — fix that first
  ```

### 3.4 — Verify

From M5 or M4:

```bash
tailscale ping beast      # replace with the actual node name
ssh beast                  # via Tailscale's MagicDNS
```

If `tailscale ping` says "via DERP" only and never goes direct, that's fine for connectivity — the Beast may be behind a stricter NAT than usual. Re-enable / re-verify Tailscale SSH or your existing SSH config and you're back.

---

## Phase 4 — Make this not happen again

Three preventives, in order of payoff:

1. **Disable key expiry for the Beast** in the Tailscale admin console. Servers should not need a human to re-auth them after a kernel update or downtime. ([Tailscale KB 1028](https://tailscale.com/kb/1028/key-expiry/))
2. **Bake an auth-key recovery path**: store a reusable Tailscale auth key in `/root/.tailscale-authkey` (chmod 600), and a systemd one-shot that runs `tailscale up --authkey file:/root/.tailscale-authkey --ssh ...` if `tailscale status` reports `NeedsLogin`. Pattern from [Tailscale `--authkey file:` support](https://www.reddit.com/r/NixOS/comments/10qyea6/). Rotate the key quarterly.
3. **Never lock SSH to Tailscale-only without a break-glass**: keep port 22 open from a small allowlist of static IPs (your Newcastle office IP, your phone-hotspot range, or a Hetzner-internal management subnet), so a Tailscale outage doesn't lock you out of your own dedicated box. The lesson is in [the Reddit Hetzner recovery thread](https://www.reddit.com/r/hetzner/comments/1pf3coy/).

---

## Appendix A — Installed OS won't boot at all

Symptoms: KVM console shows GRUB rescue prompt, `(initramfs)`, kernel panic, or `mdadm: Cannot start dirty degraded array`. Likely after a disk swap or unclean reset.

Procedure (close paraphrase of [blog.prica.ee Hetzner RAID recovery](https://blog.prica.ee/hetzner-dedicated-server-software-raid-drive-replacement/) and [Hetzner Proxmox install tutorial](https://community.hetzner.com/tutorials/install-and-configure-proxmox_ve/de/)):

1. Re-activate rescue in Robot, reboot into it.
2. Identify disks: `lsblk`, `cat /proc/mdstat`.
3. Assemble arrays: `mdadm --assemble --scan`.
4. Mount the real root, chroot in:

   ```bash
   mount /dev/md2 /mnt          # adjust to your layout
   mount /dev/md1 /mnt/boot     # if separate
   mount --bind /dev  /mnt/dev
   mount --bind /proc /mnt/proc
   mount --bind /sys  /mnt/sys
   chroot /mnt /bin/bash
   ```

5. Reinstall GRUB to both disks: `grub-install /dev/nvme0n1 && grub-install /dev/nvme1n1 && update-grub`.
6. Exit chroot, unmount, `shutdown -r now`. Confirm rescue is deactivated in Robot before the reboot.

If RAID is in a state you don't fully understand, **stop and open a Hetzner support ticket** before doing destructive operations. They will rescue → mount → diagnose for you on dedicated hardware. This is what they're for.

---

## Sources

- [Tailscale issue #367 — how to re-authenticate on Linux](https://github.com/tailscale/tailscale/issues/367)
- [Tailscale issue #9382 — machine identity lives in tailscaled.state](https://github.com/tailscale/tailscale/issues/9382)
- [Tailscale KB 1028 — key expiry, disable for servers](https://tailscale.com/kb/1028/key-expiry/)
- [OPNsense forum — needsLogin after update, fixed by renewed key](https://forum.opnsense.org/index.php?topic=45260.0)
- [CSDN — failed to connect to local tailscaled walkthrough](https://blog.csdn.net/weixin_44212848/article/details/144086815)
- [Hetzner Cloud API — disable rescue mode behaviour](https://306b3e51cy.apidog.io/api-3536571)
- [blog.prica.ee — Hetzner dedicated RAID/disk recovery in rescue](https://blog.prica.ee/hetzner-dedicated-server-software-raid-drive-replacement/)
- [Hetzner Community — Proxmox/Debian install via rescue + installimage](https://community.hetzner.com/tutorials/install-and-configure-proxmox_ve/de/)
- [Reddit r/hetzner — recent recovery (root login failed, rescue mode)](https://www.reddit.com/r/hetzner/comments/1pf3coy/urgent_need_help_recovering_hetzner_server_root/)
- [dev.to — Tailscale conflict with VPN firewall mark](https://dev.to/yulieff/how-to-run-tailscale-and-mullvad-together-on-manjaro-linux-25ke)

## Tier notes (min-rule)

- Procedure tier: **STRUCTURED**. Built from documented Tailscale/Hetzner failure modes; not yet measured against this specific Beast instance.
- Becomes **MEASURED** once Phase 1 detection is run and outputs are recorded.
- The diagnosis "still in rescue" or "expired key" is **INTUITED** until Phase 1 confirms. Don't promote to MEASURED until you've run the commands.
