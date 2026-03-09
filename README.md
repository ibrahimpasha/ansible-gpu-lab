# Ansible GPU Lab — Quick Reference

```
  WHAT IS THIS?
  ═══════════════════════════════════════════════════════════

  This project manages your NVIDIA GPU machines with Ansible.
  One command from your control node configures drivers,
  Docker, monitoring, and ML environments across all nodes.

  YOU (Control Node)                    MANAGED NODES
  ┌──────────────────┐                 ┌──────────────────┐
  │  ansible-gpu-lab/│    SSH          │  RTX 5080 PC     │
  │  Playbooks       │────────────────►│  192.168.1.10    │
  │  Roles           │                 └──────────────────┘
  │  Inventory       │    SSH          ┌──────────────────┐
  │                  │────────────────►│  RTX 3080 PC     │
  │                  │                 │  192.168.1.11    │
  │                  │                 └──────────────────┘
  │                  │    SSH          ┌──────────────────┐
  │                  │────────────────►│  Jetson Orin Nano│
  │                  │                 │  192.168.1.12    │
  └──────────────────┘                 └──────────────────┘

  No agents installed on targets — just Python + SSH.
```

---

## Before You Touch Any Files

```
  PREREQUISITES CHECKLIST
  ═══════════════════════════════════════════════════════════

  [ ] 1. Install Ansible on control node
        sudo apt install -y ansible    OR    pip install ansible

  [ ] 2. SSH server running on ALL managed nodes
        sudo apt install -y openssh-server
        sudo systemctl enable --now ssh

  [ ] 3. SSH key auth set up (no passwords)
        ssh-keygen -t ed25519 -C "ansible-control"
        ssh-copy-id ibrah@192.168.1.10
        ssh-copy-id ibrah@192.168.1.11
        ssh-copy-id ibrah@192.168.1.12

  [ ] 4. Test SSH works WITHOUT password prompt
        ssh ibrah@192.168.1.11 "hostname"
        ssh ibrah@192.168.1.12 "hostname"

  If SSH fails, NOTHING else will work.
```

---

## File Creation Order

Don't create everything at once. Follow this order — each step
builds on the previous one.

```
  BUILD ORDER
  ═══════════════════════════════════════════════════════════

  STEP 1: Foundation (get "ping" working)
  ────────────────────────────────────────
  Create these two files FIRST:

    ansible.cfg  ──► tells Ansible where inventory is, basic settings
    inventory.ini ──► lists your machines, groups, IPs

  TEST IT:
    ansible all -m ping
    ──► if you get "pong" from all 3 nodes, move on
    ──► if not, fix SSH / IPs / usernames before continuing

         ┌─────────────┐
         │ ansible.cfg │──► points to inventory.ini
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │inventory.ini│──► defines hosts + groups
         └──────┬──────┘
                │
          ansible all -m ping
                │
           pong? ───► YES ──► continue
                │
                NO
                │
           fix SSH keys / IPs first


  STEP 2: First Playbook (see Ansible do real work)
  ─────────────────────────────────────────────────
  Create:

    gpu_check.yml  ──► runs nvidia-smi on all nodes, shows GPU info

  TEST IT:
    ansible-playbook gpu_check.yml
    ansible-playbook gpu_check.yml --limit jetson


  STEP 3: Variables (teach Ansible the differences)
  ─────────────────────────────────────────────────
  Create:

    group_vars/all.yml          ──► shared settings (timezone, packages)
    group_vars/gpu_desktop.yml  ──► desktop-specific (driver ver, gpu_type)
    group_vars/jetson.yml       ──► jetson-specific (tegra, jetpack ver)
    host_vars/rtx5080.yml       ──► per-host overrides
    host_vars/rtx3080.yml       ──► per-host overrides
    host_vars/orin-nano.yml     ──► per-host overrides

  WHY: Desktop GPUs use PPA drivers. Jetson uses JetPack.
       Variables + conditionals handle this split.


  STEP 4: Roles (organize into reusable units)
  ─────────────────────────────────────────────
  Create roles in this order (each depends on the previous):

    roles/common/          ──► packages, SSH, timezone (no GPU stuff)
    roles/nvidia_driver/   ──► install/verify NVIDIA drivers
    roles/docker_nvidia/   ──► Docker + NVIDIA Container Toolkit
    roles/gpu_monitor/     ──► monitoring service + systemd
    roles/ml_environment/  ──► ML workspace with Docker Compose


  STEP 5: Master Playbook (tie it all together)
  ─────────────────────────────────────────────
  Create:

    site.yml  ──► runs all roles in correct order

  TEST IT:
    ansible-playbook site.yml --check --diff    (dry run first!)
    ansible-playbook site.yml                   (apply for real)
    ansible-playbook site.yml --limit jetson    (one group only)
```

---

## Project Map

```
  FILE MAP — WHAT EACH FILE DOES
  ═══════════════════════════════════════════════════════════

  ansible-gpu-lab/
  │
  │── ansible.cfg ·················· Ansible settings
  │                                  (inventory path, sudo config,
  │                                   output format, timeouts)
  │
  │── inventory.ini ················ WHO to manage
  │                                  (IPs, users, groups)
  │
  │── site.yml ····················· MASTER playbook
  │                                  (runs all roles in order)
  │
  │── gpu_check.yml ················ Standalone: quick GPU health check
  │
  │── group_vars/ ·················· Variables by GROUP
  │   │── all.yml ··················  applies to every host
  │   │── gpu_desktop.yml ··········  only gpu_desktop group
  │   └── jetson.yml ···············  only jetson group
  │
  │── host_vars/ ··················· Variables by HOST (overrides group)
  │   │── rtx5080.yml
  │   │── rtx3080.yml
  │   └── orin-nano.yml
  │
  └── roles/ ······················· Reusable automation units
      │
      │── common/ ·················· Base setup for ALL nodes
      │   │── tasks/main.yml ·······  timezone, apt, pip, SSH
      │   └── handlers/main.yml
      │
      │── nvidia_driver/ ··········· NVIDIA driver management
      │   │── tasks/main.yml ·······  PPA for desktop, JetPack for Jetson
      │   │── handlers/main.yml ····  reboot after driver install
      │   └── vars/main.yml
      │
      │── docker_nvidia/ ··········· Docker + GPU runtime
      │   │── tasks/main.yml ·······  Docker CE + nvidia-container-toolkit
      │   │── handlers/main.yml ····  restart docker
      │   └── templates/
      │       └── daemon.json.j2 ···  Docker daemon config for NVIDIA
      │
      │── gpu_monitor/ ············· GPU monitoring service
      │   │── tasks/main.yml ·······  deploy script + systemd service
      │   │── handlers/main.yml ····  restart monitor
      │   │── templates/
      │   │   └── gpu_monitor.service.j2   systemd unit
      │   └── files/
      │       └── gpu_monitor.py ···  Python script (temp + mem alerts)
      │
      └── ml_environment/ ·········· ML workspace
          │── tasks/main.yml ·······  create dirs, deploy compose file
          └── templates/
              └── docker-compose.gpu.yml.j2   PyTorch + Jupyter + DCGM
```

---

## Key Concepts to Remember

### Inventory Groups

```
  HOST GROUPS — HOW TARGETING WORKS
  ═══════════════════════════════════════════════════════════

  all
  └── nvidia              ◄── ansible nvidia -m ping
      ├── gpu_desktop      ◄── ansible gpu_desktop -m shell -a "nvidia-smi"
      │   ├── rtx5080      ◄── ansible rtx5080 -m setup
      │   └── rtx3080
      └── jetson            ◄── ansible jetson -m shell -a "cat /etc/nv_tegra_release"
          └── orin-nano

  nvidia:children means gpu_desktop + jetson are sub-groups of nvidia.
  Target any level: all, nvidia, gpu_desktop, jetson, or a single host.
```

### Variable Precedence

```
  VARIABLE PRECEDENCE — WHO WINS?
  ═══════════════════════════════════════════════════════════

  LOWEST PRIORITY                          HIGHEST PRIORITY
  ──────────────────────────────────────────────────────────►

  role defaults    inventory    group_vars   host_vars   play vars   -e flag
  roles/x/         inventory    group_vars/  host_vars/  vars: in    command
  defaults/        .ini         gpu_desktop  rtx5080     playbook    line
  main.yml         [group:vars] .yml         .yml                    ALWAYS
                                                                     WINS

  Example: if gpu_desktop.yml says nvidia_driver_version: "570"
           and rtx5080.yml says nvidia_driver_version: "560"
           ──► rtx5080 gets 560, rtx3080 gets 570
```

### Desktop vs Jetson — The Key Split

```
  WHY TWO PATHS?
  ═══════════════════════════════════════════════════════════

  Desktop (RTX 5080/3080)              Jetson (Orin Nano)
  ─────────────────────                ─────────────────────
  gpu_type: discrete                   gpu_type: tegra
  Arch: x86_64                         Arch: aarch64 (ARM)
  Driver: install from PPA             Driver: comes with JetPack
  CUDA: install separately             CUDA: bundled in JetPack
  DCGM: yes                            DCGM: no (not supported)
  Docker arch: amd64                   Docker arch: arm64

  The roles use "when: gpu_type == ..." to handle this split.
  group_vars/gpu_desktop.yml and group_vars/jetson.yml set gpu_type.
```

### Role Execution Flow

```
  WHAT HAPPENS WHEN YOU RUN: ansible-playbook site.yml
  ═══════════════════════════════════════════════════════════

  site.yml calls roles in order:
  ┌──────────────────────────────────────────────────────┐
  │                                                      │
  │  1. common ──────► all nvidia hosts                  │
  │     (apt, pip, SSH, timezone)                        │
  │              │                                       │
  │  2. nvidia_driver ──► all nvidia hosts               │
  │     (PPA install OR JetPack verify)                  │
  │              │                                       │
  │  3. docker_nvidia ──► all nvidia hosts               │
  │     (Docker CE + nvidia-container-toolkit)           │
  │              │                                       │
  │  4. gpu_monitor ──► all nvidia hosts                 │
  │     (monitoring script + systemd service)            │
  │              │                                       │
  │  5. ml_environment ──► gpu_desktop ONLY              │
  │     (Docker Compose: PyTorch + Jupyter)              │
  │                                                      │
  └──────────────────────────────────────────────────────┘

  Each role:
    tasks/main.yml   ──► runs the tasks (the actual work)
    handlers/main.yml ──► runs ONLY if a task says "notify"
    templates/*.j2   ──► Jinja2 files, variables get filled in
    files/*          ──► static files, copied as-is
    vars/main.yml    ──► role-specific variables
```

### Handlers — When Do They Fire?

```
  HANDLER FLOW
  ═══════════════════════════════════════════════════════════

  Task runs ──► Did something CHANGE? ──► YES ──► notify handler
                       │                              │
                       NO                        (queued, runs
                       │                         at END of all
                       ▼                         tasks in play)
                 nothing happens

  Example:
    Install nvidia-container-toolkit
         │
         ▼
    Changed? ── YES ──► notify: restart docker
         │                        │
         NO                 (waits until all tasks done)
         │                        │
    (docker stays as-is)    ──► systemd restart docker
```

---

## Common Commands

```
  COMMANDS YOU'LL USE MOST
  ═══════════════════════════════════════════════════════════

  # Test connectivity
  ansible all -m ping

  # Quick GPU check (ad-hoc)
  ansible nvidia -m shell -a "nvidia-smi"

  # Run the standalone playbook
  ansible-playbook gpu_check.yml

  # Dry run (shows what WOULD change, changes nothing)
  ansible-playbook site.yml --check --diff

  # Run everything for real
  ansible-playbook site.yml

  # Run only on desktop GPUs
  ansible-playbook site.yml --limit gpu_desktop

  # Run only on Jetson
  ansible-playbook site.yml --limit jetson

  # Run with verbose output (debugging)
  ansible-playbook site.yml -v      (or -vv, -vvv for more)

  # Override a variable from command line
  ansible-playbook site.yml -e "nvidia_driver_version=560"
```

---

## Troubleshooting

```
  WHEN THINGS BREAK
  ═══════════════════════════════════════════════════════════

  "ping" fails?
  ──► check SSH: ssh ibrah@192.168.1.XX "hostname"
  ──► check inventory.ini IPs and ansible_user
  ──► check ansible.cfg points to inventory.ini

  Task fails on Jetson but works on desktop?
  ──► check "when:" conditions use correct gpu_type
  ──► check group_vars/jetson.yml has the right values
  ──► Jetson ARM packages differ from x86 — module might not exist

  "Permission denied"?
  ──► add "become: true" to the play or task
  ──► check become_ask_pass in ansible.cfg
  ──► ensure user has sudo without password (or set ask_pass)

  Handler didn't run?
  ──► handlers only fire when a task reports "changed"
  ──► if task shows "ok" (not changed), handler is skipped
  ──► use --check mode to preview without triggering handlers
```
