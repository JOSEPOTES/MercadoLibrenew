[Setup]
AppName=Extractor Carlider
AppVersion=1.0
DefaultDirName={pf}\\ExtractorCarlider
DefaultGroupName=Extractor Carlider
OutputDir=.
OutputBaseFilename=ExtractorCarliderSetup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\\Spanish.isl"

[Files]
Source: "dist\\extractor_web.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Extractor Carlider"; Filename: "{app}\\extractor_web.exe"
Name: "{userdesktop}\\Extractor Carlider"; Filename: "{app}\\extractor_web.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un icono en el escritorio"; GroupDescription: "Opciones adicionales:"