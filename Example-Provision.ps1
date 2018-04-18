
Configuration Example {
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

        Script RemoveExisting
        {
            SetScript = {
                Remove-Item -Path $Using:ConfigurationData.AllNodes[0].WorkFolder -Force -ErrorAction SilentlyContinue
                Remove-Item -Path $Using:ConfigurationData.AllNodes[0].ZipFile -Force -ErrorAction SilentlyContinue
                Remove-Item -Path $Using:ConfigurationData.AllNodes[0].ExtractedFolder -Recurse -Force -ErrorAction SilentlyContinue
            }
            TestScript = {
                return $false # Always run, but this will make it in a not desired state, how to fix?
            }
            GetScript = {
                return @{
                    Result = $false
                }
            }
            DependsOn = "[Script]EnableTLS12"
        }

        File WorkFolder 
        {
            DestinationPath = $ConfigurationData.AllNodes[0].WorkFolder
            Ensure = "Present"
            Type = "Directory"
            DependsOn = "[Script]RemoveExisting"
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