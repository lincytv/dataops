---
layout: default
description: How to solve an alert for high run disk usage.
title: Disk Usage is High boot partition
service: doctor
runbook-name: Disk Usage is High boot partition
tags: oss, bluemix, doctor
link: /doctor/Runbook_Disk_Usage_is_High_boot_partition.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Purpose
This runbook is intended to clean up boot partition base on the follow ubuntu wiki https://askubuntu.com/questions/345588/what-is-the-safest-way-to-clean-up-boot-partition.

## Technical Details
If apt-get isn't functioning because your /boot is at 100%, you'll need to clean out /boot first. This likely has caught a kernel upgrade in a partial install which means apt has pretty much froze up entirely and will keep telling you to run apt-get -f install even though that command keeps failing.


## Instructions to Fix

The follow steps can be run if the disk does not reach 100% of usage. If does follow the last section.
You must have sudo access to be able to proceed with this runbook.

## Step 1. Confirm the disk usage is high in the boot partition
  * Login [{{wukong-portal-name}}]({{wukong-portal-link}}).
  * Select **Remote Command**.
  * Find the environment reported in the alert using the _Filter Environment Name_.
  * Check the environment.
  * Input the follow commands in the _shell commnad_ text box:
    - `df -h /boot` to confirm that the disk usage is really higher than 90 percents.
    ```
      Filesystem      Size  Used Avail Use% Mounted on
      /dev/xvda1      240M  210M   18M  93% /boot
    ```
  * Click **Run** to execute the above commands.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/remote_cmd_1.png)

  * If  **Remote Command** and WuKong keeper doesn't work, try WebSSH from Taishan or W3 BoshCli, then SSH to doctor agent.
  * Click `SSH` button, login using your sso ID and password.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/web_ssh/web-ssh-button.png){:width="639px"}
  * SSH to doctor agent .
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/web_ssh/web-ssh-boshcli.png){:width="639px" height="422px"}
  * Then try to restart the doctor-keeper process , after the keeper restated, go to next step to clear disk usage:
  `sudo supervisorctl restart doctor_keeper`


## Step 2. Check your kernel version

  Run `uname -r` It will show you the in-use kernel image.
  ```
    sshhub@wukong-portal-54b4cf8c89-k825s:~$ uname -r
    4.4.0-139-generic
  ```

## Step 3. Get all installed kernels

  Run `dpkg --list 'linux-image*' | grep ^ii`  it will list all kernels.
  ```
  root@doctor:~# dpkg --list 'linux-image*' | grep ^ii
  ii  linux-image-4.4.0-127-generic       4.4.0-127.153 amd64        Linux kernel image for version 4.4.0 on 64 bit x86 SMP
  ii  linux-image-4.4.0-130-generic       4.4.0-130.156 amd64        Linux kernel image for version 4.4.0 on 64 bit x86 SMP
  ii  linux-image-4.4.0-133-generic       4.4.0-133.159 amd64        Linux kernel image for version 4.4.0 on 64 bit x86 SMP
  ii  linux-image-4.4.0-138-generic       4.4.0-138.164 amd64        Linux kernel image for version 4.4.0 on 64 bit x86 SMP
  ii  linux-image-4.4.0-139-generic       4.4.0-139.165 amd64        Linux kernel image for version 4.4.0 on 64 bit x86 SMP
  ii  linux-image-4.4.0-141-generic       4.4.0-141.167 amd64        Linux kernel image for version 4.4.0 on 64 bit x86 SMP
  ii  linux-image-4.4.0-142-generic       4.4.0-142.168 amd64        Linux kernel image for version 4.4.0 on 64 bit x86 SMP
  ii  linux-image-extra-4.4.0-127-generic 4.4.0-127.153 amd64        Linux kernel extra modules for version 4.4.0 on 64 bit x86 SMP
  ii  linux-image-virtual                 4.4.0.142.148 amd64        This package will always depend on the latest minimal generic kernel image.

  ```
## Step 4. Remove old kernels

  Use the follow command to remove the old kernels `apt-get remove linux-image-VERSION`.
  Replace VERSION with the version of the kernel you want to remove
  Example `apt-get remove linux-image-4.4.0-127-generic`
  For this example you want to delete 127, 130, 133 and 138 you need to leave the newer versions in this case 141 and 142.

  ```
  root@doctor:~# apt-get remove linux-image-4.4.0-127-generic
  Reading package lists... Done
  Building dependency tree       
  Reading state information... Done
  The following packages were automatically installed and are no longer required:
  crda iw linux-headers-4.4.0-127 linux-headers-4.4.0-127-generic linux-headers-4.4.0-130 linux-headers-4.4.0-130-generic linux-headers-4.4.0-133
  linux-headers-4.4.0-133-generic linux-headers-4.4.0-138 linux-headers-4.4.0-138-generic linux-image-4.4.0-130-generic linux-image-4.4.0-133-generic
  linux-image-4.4.0-138-generic wireless-regdb
  Use 'sudo apt autoremove' to remove them.
  The following packages will be REMOVED:
  linux-image-4.4.0-127-generic linux-image-extra-4.4.0-127-generic
  0 upgraded, 0 newly installed, 2 to remove and 86 not upgraded.
  After this operation, 224 MB disk space will be freed.
  Do you want to continue? [Y/n]
  (Reading database ... 236219 files and directories currently installed.)
  Removing linux-image-extra-4.4.0-127-generic (4.4.0-127.153) ...
  run-parts: executing /etc/kernel/postinst.d/apt-auto-removal 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  run-parts: executing /etc/kernel/postinst.d/initramfs-tools 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  update-initramfs: Generating /boot/initrd.img-4.4.0-127-generic
  W: mdadm: /etc/mdadm/mdadm.conf defines no arrays.
  run-parts: executing /etc/kernel/postinst.d/unattended-upgrades 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  run-parts: executing /etc/kernel/postinst.d/update-notifier 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  run-parts: executing /etc/kernel/postinst.d/x-grub-legacy-ec2 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  Searching for GRUB installation directory ... found: /boot/grub
  Searching for default file ... found: /boot/grub/default
  Testing for an existing GRUB menu.lst file ... found: /boot/grub/menu.lst
  Searching for splash image ... none found, skipping ...
  Found kernel: /vmlinuz-4.4.0-127-generic
  Found kernel: /vmlinuz-4.4.0-142-generic
  Found kernel: /vmlinuz-4.4.0-141-generic
  Found kernel: /vmlinuz-4.4.0-139-generic
  Found kernel: /vmlinuz-4.4.0-138-generic
  Found kernel: /vmlinuz-4.4.0-133-generic
  Found kernel: /vmlinuz-4.4.0-130-generic
  Found kernel: /vmlinuz-4.4.0-127-generic
  Updating /boot/grub/menu.lst ... done

  run-parts: executing /etc/kernel/postinst.d/zz-update-grub 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  Generating grub configuration file ...
  Found linux image: /boot/vmlinuz-4.4.0-142-generic
  Found initrd image: /boot/initrd.img-4.4.0-142-generic
  Found linux image: /boot/vmlinuz-4.4.0-141-generic
  Found initrd image: /boot/initrd.img-4.4.0-141-generic
  Found kernel: /vmlinuz-4.4.0-141-generic
  Found linux image: /boot/vmlinuz-4.4.0-139-generic
  Found initrd image: /boot/initrd.img-4.4.0-139-generic
  Found linux image: /boot/vmlinuz-4.4.0-138-generic
  Found initrd image: /boot/initrd.img-4.4.0-138-generic
  Found linux image: /boot/vmlinuz-4.4.0-133-generic
  Found initrd image: /boot/initrd.img-4.4.0-133-generic
  Found linux image: /boot/vmlinuz-4.4.0-130-generic
  Found initrd image: /boot/initrd.img-4.4.0-130-generic
  Found linux image: /boot/vmlinuz-4.4.0-127-generic
  Found initrd image: /boot/initrd.img-4.4.0-127-generic
  done
  Removing linux-image-4.4.0-127-generic (4.4.0-127.153) ...
  Examining /etc/kernel/postrm.d .
  run-parts: executing /etc/kernel/postrm.d/initramfs-tools 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  update-initramfs: Deleting /boot/initrd.img-4.4.0-127-generic
  run-parts: executing /etc/kernel/postrm.d/x-grub-legacy-ec2 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  Searching for GRUB installation directory ... found: /boot/grub
  Searching for default file ... found: /boot/grub/default
  Testing for an existing GRUB menu.lst file ... found: /boot/grub/menu.lst
  Searching for splash image ... none found, skipping ...
  Found kernel: /vmlinuz-4.4.0-127-generic
  Found kernel: /vmlinuz-4.4.0-142-generic
  Found kernel: /vmlinuz-4.4.0-141-generic
  Found kernel: /vmlinuz-4.4.0-139-generic
  Found kernel: /vmlinuz-4.4.0-138-generic
  Found kernel: /vmlinuz-4.4.0-133-generic
  Found kernel: /vmlinuz-4.4.0-130-generic
  Updating /boot/grub/menu.lst ... done
  run-parts: executing /etc/kernel/postrm.d/zz-update-grub 4.4.0-127-generic /boot/vmlinuz-4.4.0-127-generic
  Generating grub configuration file ...
  Found linux image: /boot/vmlinuz-4.4.0-142-generic
  Found initrd image: /boot/initrd.img-4.4.0-142-generic
  Found linux image: /boot/vmlinuz-4.4.0-141-generic
  Found initrd image: /boot/initrd.img-4.4.0-141-generic
  Found linux image: /boot/vmlinuz-4.4.0-139-generic
  Found initrd image: /boot/initrd.img-4.4.0-139-generic
  Found linux image: /boot/vmlinuz-4.4.0-138-generic
  Found initrd image: /boot/initrd.img-4.4.0-138-generic
  Found linux image: /boot/vmlinuz-4.4.0-133-generic
  Found initrd image: /boot/initrd.img-4.4.0-133-generic
  Found linux image: /boot/vmlinuz-4.4.0-130-generic
  Found initrd image: /boot/initrd.img-4.4.0-130-generic
  done
  ```

  You may get the follow questions select the default and continue.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/os_boot/boot_grub_menu.png){:width="639px"}


## Step 5. Permanently remove old kernels

  When you're done removing the older kernels, you can run this to remove the packages you don’t need anymore.
  Run `apt-get autoremove`

  ```
  root@doctor:~# apt-get autoremove
  Reading package lists... Done
  Building dependency tree       
  Reading state information... Done
  The following packages will be REMOVED:
    crda iw linux-headers-4.4.0-130 linux-headers-4.4.0-130-generic linux-headers-4.4.0-133 linux-headers-4.4.0-133-generic linux-headers-4.4.0-138
    linux-headers-4.4.0-138-generic linux-image-4.4.0-130-generic linux-image-4.4.0-133-generic linux-image-4.4.0-138-generic wireless-regdb
  0 upgraded, 0 newly installed, 12 to remove and 86 not upgraded.
  After this operation, 440 MB disk space will be freed.
  Do you want to continue? [Y/n]
  ```

## Step 6. Update grub kernel list

  Run the follow command to upgrade grub kernel list `update-grub`

  ```
  root@doctor:~# update-grub
  Generating grub configuration file ...
  Found linux image: /boot/vmlinuz-4.4.0-142-generic
  Found initrd image: /boot/initrd.img-4.4.0-142-generic
  Found linux image: /boot/vmlinuz-4.4.0-141-generic
  Found initrd image: /boot/initrd.img-4.4.0-141-generic
  Found linux image: /boot/vmlinuz-4.4.0-139-generic
  Found initrd image: /boot/initrd.img-4.4.0-139-generic
  Found linux image: /boot/vmlinuz-4.4.0-138-generic
  Found initrd image: /boot/initrd.img-4.4.0-138-generic
  Found linux image: /boot/vmlinuz-4.4.0-133-generic
  Found initrd image: /boot/initrd.img-4.4.0-133-generic
  Found linux image: /boot/vmlinuz-4.4.0-130-generic
  Found initrd image: /boot/initrd.img-4.4.0-130-generic
  done
  ```

  Disk space should be good after complete this steps. After confirmed you are done.

## This is only if you can't use apt to clean up due to a 100% full /boot

  If apt-get isn't functioning because your /boot is at 100%, you'll need to clean out /boot first. This likely has caught a kernel upgrade in a partial install which means apt has pretty much froze up entirely and will keep telling you to run apt-get -f install even though that command keeps failing.

  1. Get the current kernel version from Step 2.
  2. Get the list of kernel images and determine what you can do without. This command will show installed kernels except the currently running one ``` dpkg --list 'linux-image*'|awk '{ if ($1=="ii") print $2}'|grep -v `uname -r` ``` or you can follow step 3.
  > Note the two newest versions in the list. You don't need to worry about the running one as it isn't listed here.

  3. Craft a command to delete all files in /boot for kernels that don't matter to you using brace expansion to keep you sane. Remember to exclude the current and two newest kernel images. Example: `rm -rf /boot/*-3.2.0-{23,45,49,51,52,53,54,55}-*`. You can also use a range with the syntax {80..84}.

  4. Run `apt-get -f install` to clean up what's making apt grumpy about a partial install.

  > If you run into an error that includes a line like `Internal Error: Could not find image (/boot/vmlinuz-3.2.0-56-generic)`, then run the command `apt-get purge linux-image-3.2.0-56-generic` (with your appropriate version).

  5. Finally, `apt-get autoremove` to clear out the old kernel image packages that have been orphaned by the manual boot clean.

  > Suggestion, run `apt-get update` and `apt-get upgrade` to take care of any upgrades that may have backed up while waiting for you to discover the full /boot partition.


## Notes and Special Considerations
The above steps can normally be done from **Remote Command** for the environment, or in an ssh session.
In case neither Remote Command nor ssh from WuKong -> Doctor Keeper works, [Doctor Tips and Techniques](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Doctor_Oncall_Tips_and_Techniques.html) includes other ways to get the ssh session from Doctor.

{% include {{site.target}}/tips_and_techniques.html %}
