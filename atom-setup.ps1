$fred = (Get-Content my-packages.txt)
$env:PYTHON = "C:\Python27\python.exe"
ForEach-Object -InputObject $fred { apm install $_ }