
Configuration UninstallExample {
    Import-DscResource -ModuleName "PSDesiredStateConfiguration"
    Import-DscResource -ModuleName "xPSDesiredStateConfiguration"

    $ConfigurationData = @{
    AllNodes = @(
        @{
            NodeName = 'localhost'
            PSDscAllowPlainTextPassword = $true
            PsDscAllowDomainUser = $true
            ZipFile = "C:\Users\grave\Desktop\DSC Example\Work\master.zip"
            WorkFolder = "C:\Users\grave\Desktop\DSC Example\Work"
            ExtractedFolder = "C:\Users\grave\Desktop\DSC Example\Work\extracted"
            DownloadUri = "https://github.com/Atheuz/Falcon-Case/archive/master.zip"
        })
    }

    Node 'localhost'
    {
        File RemoveExistingWorkFolder 
        {
            DestinationPath = $ConfigurationData.AllNodes[0].WorkFolder
            Ensure = "Absent"
            Type = "Directory"
        }
    }
}

Configuration InstallExample {
    Import-DscResource -ModuleName "PSDesiredStateConfiguration"
    Import-DscResource -ModuleName "xPSDesiredStateConfiguration"   
    $ConfigurationData = @{
    AllNodes = @(
        @{
            NodeName = 'localhost'
            PSDscAllowPlainTextPassword = $true
            PsDscAllowDomainUser = $true
            ZipFile = "C:\Users\grave\Desktop\DSC Example\Work\master.zip"
            WorkFolder = "C:\Users\grave\Desktop\DSC Example\Work"
            ExtractedFolder = "C:\Users\grave\Desktop\DSC Example\Work\extracted"
            DownloadUri = "https://github.com/Atheuz/Falcon-Case/archive/master.zip"
        })
    }

    $state = $false

    Node 'localhost'
    {
        Script EnableTLS12
        {
            SetScript = {
                [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol.toString() + ', ' + [Net.SecurityProtocolType]::Tls12
            }
            TestScript = {
               return ([Net.ServicePointManager]::SecurityProtocol -match 'Tls12')
            }
            GetScript = {
                return @{
                    Result = ([Net.ServicePointManager]::SecurityProtocol -match 'Tls12')
                }
            }
        }

        File WorkFolder 
        {
            DestinationPath = $ConfigurationData.AllNodes[0].WorkFolder
            Ensure = "Present"
            Type = "Directory"
            DependsOn = "[Script]EnableTLS12"
        }

        xRemoteFile ZipFile
        {
            DependsOn = "[File]WorkFolder"
            Uri = $ConfigurationData.AllNodes[0].DownloadUri
            DestinationPath = $ConfigurationData.AllNodes[0].ZipFile
            MatchSource = $false
        }
        
        Archive ExtractFile 
        {
            Ensure = "Present"
            DependsOn = "[xRemoteFile]ZipFile"
            Path = $ConfigurationData.AllNodes[0].ZipFile
            Destination = $ConfigurationData.AllNodes[0].ExtractedFolder
        }
    }
}