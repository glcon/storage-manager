param (
    [Parameter(Mandatory=$true)]
    [string]$DirPath
)

# Calculate total size in bytes
$size = (Get-ChildItem -Path $DirPath -Recurse -File -ErrorAction SilentlyContinue | 
         Measure-Object -Property Length -Sum).Sum

Write-Output $size