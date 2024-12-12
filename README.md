# DerSauger

**Installation:**

### Only compatible with win10,win11 and subsequent versions which support winget

Go to the releases page:  
[https://github.com/GrafKrausula/DerSauger/releases](https://github.com/GrafKrausula/DerSauger/releases)

Look for the latest release (at the very top) and click on the `.exe` file to download it.  
Then, run the file.

---------------------------------------------------------------

**You're all set!**

**FAQ:**

**Q:** The installer aborts/fails?!?
**A:** Ensure that "winget" works.

The WinGet command line tool is only supported on Windows 10 1709 (build 16299) or later at this time. WinGet will not be available until you have logged into Windows as a user for the first time, triggering Microsoft Store to register the Windows Package Manager as part of an asynchronous process. If you have recently logged in as a user for the first time and find that WinGet is not yet available, you can open PowerShell and enter the following command to request this WinGet registration: Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe

https://learn.microsoft.com/en-us/windows/package-manager/winget/
https://github.com/microsoft/winget-cli

or

stolen from reddit:
"Check the version of the "App Installer" package on your laptops.

Microsoft changed all the FQDNs used by Winget some time back, which broke it.

Fk knows why they chose a solution of needing to upgrade the "App Installer" package instead of fixing it via Windows Update. And you'll need access to the MS Store to install the latest "App Installer".

It's almost as if someone is trying to push their store..."
https://github.com/microsoft/winget-cli


**Q:** I installed DerSauger and everything, but nothing is happening?!  
**A:** Please download the "Visual C++ Redistributable Packages for Visual Studio 2015, 2017, and 2019."  

- For 32-bit systems, download **"x86: vc_redist.x86.exe."**  
- For 64-bit systems, download **"x64: vc_redist.x64.exe."**  

You can find them here:  
[https://support.microsoft.com/en-gb/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0](https://support.microsoft.com/en-gb/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0)
