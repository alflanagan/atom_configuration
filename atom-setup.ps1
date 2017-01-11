# for node-gyp
$env:PYTHON = "C:\Python27\pythonw.exe"

$fred = (Get-Content my-packages.txt)
$wilma = apm list --no-color --bare --installed
$installed = $wilma.ForEach( { $_.split('@')[0] } )
$differences = Compare-Object -ReferenceObject $installed -DifferenceObject $fred

# Compare-Object returns PSCustomObject if collections are equal (???)
# but is schizo about type of return array
if ($differences.GetType().Name -ne "Object[]" -and $differences.GetType().Name -ne "Array")
{
  Write-Host "There are no differences between installed and my-packages.txt"  -ForegroundColor Cyan
  exit 0
}

$uninstalled = $differences.Where( { $_.SideIndicator -eq "=>" } )
$uninstalled = $uninstalled.ForEach( { $_.InputObject })
$extra = $differences.Where( { $_.SideIndicator -eq "<=" } )
$extra = $extra.ForEach( { $_.InputObject } )

if ($uninstalled.Count -gt 1 -or $extra[0] -ne "") {
  Write-Host "Packages In my-packages Not Installed" -ForegroundColor Red
  Write-Host $uninstalled
  Write-Host "`n"
}

if ($extra.Count -gt 1 -or $extra[0] -ne "") {
  Write-Host "Packages Installed But Not in my-packages List" -ForegroundColor Red
  Write-Host $extra
}

if ($args.Contains("--install")) {
  $uninstalled.ForEach( { apm install --no-color $_ } )
}
