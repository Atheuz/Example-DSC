
Configuration Example {
    Import-DscResource -ModuleName "PSDesiredStateConfiguration"
    Import-DscResource -ModuleName "xPSDesiredStateConfiguration"

    Node 'localhost'
    {
        xScript EnableTLS12
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

        Archive ExtractFile 
        {
            Ensure = "Present"
            DependsOn = "[xRemoteFile]ZipFile"
            Path = "C:\Users\grave\Desktop\DSC Example\Work\master.zip"
            Destination = "C:\Users\grave\Desktop\DSC Example\Work\extracted"
        }

        xRemoteFile ZipFile
        {
            DependsOn = "[File]WorkFolder"
            Uri = "https://github.com/Atheuz/Falcon-Case/archive/master.zip"
            DestinationPath = "C:\Users\grave\Desktop\DSC Example\Work\master.zip"
            MatchSource = $true
        }

        File WorkFolder 
        {
            Ensure = "Present"
            Type = "Directory"
            DestinationPath = "C:\Users\grave\Desktop\DSC Example\Work"
        }
    }


}
Example