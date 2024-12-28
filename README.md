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

The WinGet command line tool is only supported on Windows 10 1709 (build 16299) or later at this time. WinGet will not be available until you have logged into Windows as a user for the first time, triggering Microsoft Store to register the Windows Package Manager as part of an asynchronous process. If you have recently logged in as a user for the first time and find that WinGet is not yet available, you can either:

A) visit https://aka.ms/getwinget, download the installer from and install it via opening the downloaded file.

B) open PowerShell and enter the following command to request this WinGet registration: 

```Powershell
Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe
```

After installing winget, retry opening the installer.


Sources:

https://learn.microsoft.com/en-us/windows/msix/app-installer/install-update-app-installer
http://web.archive.org/web/20241217202156/https://learn.microsoft.com/en-us/windows/msix/app-installer/install-update-app-installer

https://learn.microsoft.com/en-us/windows/package-manager/winget/
http://web.archive.org/web/20241228132254/https://learn.microsoft.com/en-us/windows/package-manager/winget/

https://github.com/microsoft/winget-cli


**Q:** I completed the installer of DerSauger, but nothing is happening?!  
**A:** Please download the "Visual C++ Redistributable Packages for Visual Studio 2015, 2017, and 2019."  

- For 32-bit systems, download **"x86: vc_redist.x86.exe."**  
- For 64-bit systems, download **"x64: vc_redist.x64.exe."**  

You can find them here:  
[https://support.microsoft.com/en-gb/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0](https://support.microsoft.com/en-gb/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0)
