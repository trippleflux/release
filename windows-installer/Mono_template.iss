; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=Mono @@MONO_VERSION@@ with GTK# @@GTK_SHARP_VERSION@@
AppVerName=Mono for Windows @@MONO_VERSION@@
AppPublisher=Mono
AppPublisherURL=http://www.mono-project.com
AppSupportURL=http://www.mono-project.com/about/faq.html
AppUpdatesURL=http://www.mono-project.com/downloads/index.html
DefaultDirName={pf}\Mono-@@MONO_VERSION@@
DefaultGroupName=Mono @@MONO_VERSION@@ for Windows
AppID={{@@MONO_GUID@@}
Compression=lzma/max
;Compression=bzip/4
;Compression=zip
SolidCompression=true
DisableDirPage=false
DisableReadyPage=false
OutputBaseFilename=mono-@@MONO_VERSION@@-gtksharp-@@GTK_SHARP_VERSION@@-win32-@@MONO_REVISION@@
VersionInfoVersion=@@MONO_VERSION@@
VersionInfoDescription=Mono @@MONO_VERSION@@ with Gtk# Installer for Win32
VersionInfoCompany=Mono
InfoBeforeFile=build\mono\ReleaseNotes.txt
LicenseFile=setup-files\mono-lic.txt
WizardSmallImageFile=setup-files\installerBannerSmall256_52x52.bmp
WizardImageFile=setup-files\installerBanner256.bmp
UninstallDisplayIcon={app}\mono.ico
SetupIconFile=setup-files\mono.ico
ShowLanguageDialog=yes
AppVersion=@@MONO_VERSION@@
MinVersion=0,5.0


[Types]
Name: full; Description: Full installation
Name: compact; Description: Compact installation
Name: custom; Description: Custom installation; Flags: iscustom

[Components]
Name: mono; Description: Mono Files; Types: full compact custom; Flags: fixed
Name: gtk; Description: GTK+ 2.10 and Gnome 2.16 Files; Types: full custom
Name: gtk\gtkSharp; Description: Gtk# @@GTK_SHARP_VERSION@@ Files; Types: full custom
Name: gtk\gtkSharp\monodoc; Description: Monodoc; Types: full custom
Name: gtk\gtkSharp\geckosharp; Description: Gecko# Files; Types: full custom
Name: gtk\gtkSharp\samples; Description: Samples; Types: full custom
Name: xsp; Description: XSP files; Types: full custom
Name: xsp\xsp_shell; Description: XSP Shell Integration; Types: full custom
Name: xsp\xsp2_shell; Description: XSP 2.0 Shell Integration; Types: full custom

[Tasks]

[Files]
Source: build\mono\*; DestDir: {app}; Components: mono; Flags: ignoreversion recursesubdirs
Source: build\gdiplus.dll; DestDir: {app}\bin; Components: mono; OnlyBelowVersion: 0,5.01
Source: build\xsp\*; DestDir: {app}; Components: xsp; Flags: ignoreversion recursesubdirs
Source: build\gtk\*; DestDir: {app}; Components: gtk; Flags: ignoreversion recursesubdirs
Source: build\gtk-sharp\*; DestDir: {app}; Components: gtk\gtksharp; Flags: ignoreversion recursesubdirs
Source: build\gecko-sharp\*; DestDir: {app}; Components: gtk\gtkSharp\geckosharp; Flags: ignoreversion recursesubdirs
Source: build\samples\*; DestDir: {app}; Components: gtk\gtkSharp\samples; Flags: ignoreversion recursesubdirs
Source: build\monodoc\*; DestDir: {app}; Components: gtk\gtkSharp\monodoc; Flags: ignoreversion recursesubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[INI]
Filename: {app}\Mono.url; Section: InternetShortcut; Components: mono; Key: URL; String: http://www.mono-project.com
Filename: {app}\MonoReleaseNotes.url; Section: InternetShortcut; Components: mono; Key: URL; String: http://go-mono.com/archive/@@MONO_VERSION@@/
Filename: {app}\GtkPlus.url; Section: InternetShortcut; Components: gtk; Key: URL; String: http://www.gtk.org
Filename: {app}\GtkSharp.url; Section: InternetShortcut; Components: gtk\gtkSharp; Key: URL; String: http://gtk-sharp.sourceforge.net/index.html
Filename: {app}\Xsplocal.url; Section: InternetShortcut; Components: xsp; Key: URL; String: {code:GetURLAndPort}/index.aspx
Filename: {app}\Xsplocal2.url; Section: InternetShortcut; Components: xsp; Key: URL; String: {code:GetURLAndPort}/index2.aspx
; TODO: I'm not sure what was supposed to be at this link, so it's disabled for now
;Filename: {app}\MonoDocWeb.url; Section: InternetShortcut; Components: xsp and gtk\gtkSharp\monodoc; Key: URL; String: {code:GetURLAndPort}/header.html
; Add a link to the online mono documentation
Filename: {app}\MonoDocWeb.url; Section: InternetShortcut; Components: mono; Key: URL; String: http://www.go-mono.com/docs/

[Icons]
Name: {group}\Mono-@@MONO_VERSION@@ Command Prompt; IconFilename: {app}\mono.ico; Filename: {cmd}; Parameters: "/k ""{app}\bin\setmonopath.bat"""; Comment: Open Mono @@MONO_VERSION@@ Command Prompt
Name: {group}\Readme; Filename: {app}\ReleaseNotes.txt; Comment: Combined Installer Release Notes
Name: {group}\{cm:ProgramOnTheWeb,Mono-@@MONO_VERSION@@ Release Notes}; Filename: {app}\MonoReleaseNotes.url
Name: {group}\MonoDoc Web; Components: mono; Filename: {app}\MonoDocWeb.url
Name: {group}\Applications\Gtk# Demo; Filename: {app}\bin\GtkDemo.bat; Components: gtk\gtkSharp\samples; Comment: Gtk# Demo
Name: {group}\Applications\Sql# GTK; Filename: {app}\bin\sqlsharpgtk.bat; Components: gtk\gtkSharp\samples; Comment: SQL# GUI version
Name: {group}\Applications\Prj2Make# GTK; Filename: {app}\bin\prj2make-sharp-gtk.bat; Components: gtk\gtkSharp\samples; Comment: Makefile generator tool.
Name: {group}\Applications\Samples Directory; Filename: {app}\samples; Components: gtk\gtkSharp\samples; Comment: Gtk# samples directory
Name: {group}\Applications\Glade 3; Filename: {app}\bin\glade-3.exe; Components: gtk; Comment: Glade 3 Gui Builder
Name: {group}\Applications\Gtk Theme Selector; Filename: {app}\bin\gtkthemeselector.exe; Components: gtk; Comment: GTK Theme Selector
;Name: {group}\Applications\Monodoc Browser; IconFilename: {app}\mono.ico; Filename: {app}\bin\monodoc.bat; Components: gtk\gtkSharp\monodoc; Comment: Mono Documentation Browser
Name: {group}\XSP\XSP Test Web Server; Filename: {app}\bin\startXSP.bat; Components: xsp; Comment: ASP.NET Web Server with Sample Mono content
Name: {group}\XSP\XSP 2.0 Test Web Server; Filename: {app}\bin\startXSP2.bat; Components: xsp; Comment: ASP.NET Web Server with Sample Mono content
Name: {group}\{cm:ProgramOnTheWeb,Mono}; IconFilename: {app}\mono.ico; Filename: {app}\Mono.url
Name: {group}\{cm:UninstallProgram,Mono-@@MONO_VERSION@@ Win32}; Filename: {uninstallexe}
Name: {group}\{cm:ProgramOnTheWeb,Gtk+}; Components: gtk; Filename: {app}\GtkPlus.url
Name: {group}\{cm:ProgramOnTheWeb,Gtk#}; Components: gtk\gtkSharp; Filename: {app}\GtkSharp.url
Name: {group}\XSP\XSP Index Page; Components: xsp; Filename: {app}\Xsplocal.url
Name: {group}\XSP\XSP 2.0 Index Page; Components: xsp; Filename: {app}\Xsplocal2.url

[Registry]
Root: HKLM; Subkey: SOFTWARE\Novell\Mono; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: Software\Novell\Mono; ValueType: string; ValueName: DefaultCLR; ValueData: @@MONO_VERSION@@; Flags: uninsdeletevalue
Root: HKLM; Subkey: SOFTWARE\Novell\Mono\@@MONO_VERSION@@; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: Software\Novell\Mono\@@MONO_VERSION@@; ValueType: string; ValueName: FrameworkAssemblyDirectory; ValueData: {app}\lib; Flags: uninsdeletevalue
Root: HKLM; Subkey: Software\Novell\Mono\@@MONO_VERSION@@; ValueType: string; ValueName: MonoConfigDir; ValueData: {app}\etc; Flags: uninsdeletevalue
Root: HKLM; Subkey: Software\Novell\Mono\@@MONO_VERSION@@; ValueType: string; ValueName: SdkInstallRoot; ValueData: {app}; Flags: uninsdeletevalue
Root: HKLM; Subkey: Software\Novell\Mono\@@MONO_VERSION@@; Components: xsp; ValueType: dword; ValueName: XSPIsInstalled; ValueData: 1; Flags: uninsdeletevalue
Root: HKLM; Subkey: Software\Novell\Mono\@@MONO_VERSION@@; Components: gtk\gtkSharp; ValueType: dword; ValueName: GtkSharpIsInstalled; ValueData: 1; Flags: uninsdeletevalue
Root: HKLM; Subkey: Software\Novell\Mono\@@MONO_VERSION@@; Components: gtk; ValueType: dword; ValueName: GtkPlusDevIsInstalled; ValueData: 1; Flags: uninsdeletevalue
Root: HKLM; Subkey: SOFTWARE\Novell\Mono DefaultCLR; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: Software\Novell\Mono DefaultCLR; ValueType: string; ValueName: Installer Language; ValueData: 1033; Flags: uninsdeletevalue
; XSP Shell Integration (Thanks to Joseph Hill)
Root: HKLM; Subkey: SOFTWARE\Classes\Folder\shell\XSP WebServer @@MONO_VERSION@@; Components: xsp\xsp_shell; ValueType: string; ValueData: XSP Web Server Here @@MONO_VERSION@@; Flags: uninsdeletekey
Root: HKLM; Subkey: SOFTWARE\Classes\Folder\shell\XSP WebServer @@MONO_VERSION@@\command; Components: xsp\xsp_shell; ValueType: string; ValueData: "{app}\bin\xsp.bat --root ""%1"" --port {code:GetPort} --applications /:."; Flags: uninsdeletekey
Root: HKLM; Subkey: SOFTWARE\Classes\Folder\shell\XSP2 WebServer @@MONO_VERSION@@; Components: xsp\xsp2_shell; ValueType: string; ValueData: XSP 2.0 Web Server Here @@MONO_VERSION@@; Flags: uninsdeletekey
Root: HKLM; Subkey: SOFTWARE\Classes\Folder\shell\XSP2 WebServer @@MONO_VERSION@@\command; Components: xsp\xsp2_shell; ValueType: string; ValueData: "{app}\bin\xsp2.bat --root ""%1"" --port {code:GetPort} --applications /:."; Flags: uninsdeletekey

;[Run]
;Filename: "{app}\gacutil.exe"; Description: "Install gtk-sharp in the MS GAC"; StatusMsg: "Install Gtk# in the MS GAC"; Tasks: msgac

[UninstallDelete]
Type: files; Name: {app}\Mono.url
Type: files; Name: {app}\MonoReleaseNotes.url
Type: files; Name: {app}\GtkPlus.url
Type: files; Name: {app}\GtkSharp.url
Type: files; Name: {app}\Xsplocal.url
Type: files; Name: {app}\Xsplocal2.url
Type: files; Name: {app}\MonoDocWeb.url
;TODO: delete monodoc and gconf cruft?

[Code]
var
  PortForXSP: TInputQueryWizardPage;

Function GetMonoBasePath(strParam1 : string): string;
var
    strMonoBaseDir: String;
    bRc: Boolean;
begin
    // Get the registry value
    bRc := RegQueryStringValue(HKLM, 'SOFTWARE\Novell\Mono\@@MONO_VERSION@@', 'SdkInstallRoot',
    strMonoBaseDir
    );

    If bRc = true Then
    begin
        Result := strMonoBaseDir;
    end;
end;

// Checks to see if Mono @@MONO_VERSION@@ is Installed
Function IsMonoInstalled() : Boolean;
begin
    Result := RegValueExists(HKLM, 'SOFTWARE\Novell\Mono\@@MONO_VERSION@@', 'SdkInstallRoot');
end;

Function SayMessage(const strMsg: String; const typMsgBox: TMsgBoxType) : Integer;
begin
  Result := MsgBox(strMsg, typMsgBox, MB_OK);
end;

//These Initialize* functions must get called automatically
Function InitializeSetup : Boolean;
begin
	// Check requirements before Installation
	If IsMonoInstalled() = true Then
	begin
	 Result := false;
	 SayMessage('Mono seems to be installed.' + #13 + #10 + 'Please uninstall it and run this setup again.', mbError);
	 exit;
	end
	Result := true;
end;

procedure InitializeWizard;
begin
    { Create the pages }
    PortForXSP := CreateInputQueryPage(
        wpSelectProgramGroup,
        'Port Selection', 'What Port should XSP use?',
        'Please specify the port that XSP will use or accept the default, then click Next.'
        );

    PortForXSP.Add('Port:', False);
    PortForXSP.Values[0] := '8088';
end;

// Search and replace in a file
Procedure substituteInFile(strFileName, strOriginal, strReplacement: String);
var
	strFileContents: String;
begin
	// Read the contents of the file into a string and continue if string is found in file
	if (LoadStringFromFile(strFileName, strFileContents) = true) and (Pos(strOriginal, strFileContents) > 0)  then
	begin
		// Perform search and replace
		StringChange(strFileContents, strOriginal, strReplacement);
		// Write the changed string back out to the file
		SaveStringToFile(strFileName, strFileContents, false);
	end;
end;


Procedure WriteRootPath(const cstrBasePath: String);
var
	strFilePath, forwardSlashBasePath: String;
	FindRec: TFindRec;
	listOfDirs: Array OF String;
	numFiles, i: Longint;
begin

	forwardSlashBasePath := cstrBasePath;
	StringChange(forwardSlashBasePath, '\', '/')
  	
	listOfDirs := [
		'\bin',
		'\etc\gtk-2.0',
		'\etc\pango',
		'\lib\pkgconfig',
		'\lib\mono\gac\monodoc\1.0.0.0__0738eb9f132ed756'
	]

	numFiles := GetArrayLength(ListOfDirs);

	// List of directories and vars to replace:  bin, etc/gtk-2.0, etc/pango, lib/pkgconfig
	// lib\mono\gac\monodoc\1.0.0.0__0738eb9f132ed756\monodoc.dll.config
	// share\doc\xsp\test\bin\monodoc.dll.config (This dir doesn't exist anymore)

	for i := 0 to numFiles - 1 do
	begin
		// Iterate through all files in the directory
		if FindFirst(cstrBasePath + listOfDirs[i] + '\*', FindRec) then
		begin
			try
			repeat
  				// Skip directories
				if FindRec.Attributes and FILE_ATTRIBUTE_DIRECTORY = 0 then
					strFilePath := cstrBasePath + listOfDirs[i] + '\' + FindRec.Name;				
					substituteInFile(strFilePath, '@@DOS_MONO_INST_DIR@@', cstrBasePath)
					substituteInFile(strFilePath, '@@WIN_MONO_INST_DIR@@', forwardSlashBasePath)

  			until not FindNext(FindRec);
			finally
			FindClose(FindRec);
			end;
		end; // If
	end;  // For

	// Set the Port for XSP
	substituteInFile(cstrBasePath + '\bin\startXSP.bat', '8089', PortForXSP.Values[0]);
	substituteInFile(cstrBasePath + '\bin\startXSP2.bat', '8089', PortForXSP.Values[0]);
	
end;


Function GetURLAndPort(Param: String) : string;
var strPort: string;
begin
    strPort := PortForXSP.Values[0];
    Result := 'http://localhost:' + strPort;
end;

Function GetPort(Param: String): string;
begin
    Result := PortForXSP.Values[0];
end;

Procedure CurStepChanged(CurStep: TSetupStep);
var
 strBasePath: String;
begin
  if CurStep = ssPostInstall THEN
  begin
    // Get the var and then remove the backslash from the end
    strBasePath := RemoveBackslash(ExpandConstant('{app}'));
    // If there's a space, use the shortname
    if Pos(' ', strBasePath) <> 0 THEN
      strBasePath := GetShortName(strBasePath);
    WriteRootPath(strBasePath);
  end;
end;

Function ShouldSkipPage(PageID: Integer): Boolean;
var
  bInstallXsp: Boolean;
begin
  bInstallXsp := IsComponentSelected('xsp');
  if (bInstallXsp = false) and (PageID = PortForXSP.ID) THEN
  begin
    Result := true;
    exit;
  end;
    Result := false;
end;

