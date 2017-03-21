# for node-gyp
$env:PYTHON = "C:\Python27\pythonw.exe"
$pkg_list = "my-packages.txt"
if ($env:OS -Like "Windows*")
{
    $pkg_list = "my-windows-packages.txt"
}

$betty = New-Object System.Collections.Generic.List[System.Object] 
(Get-Content $pkg_list).ForEach( { $betty.Add($_) } )
# add auto-installed dependent pkgs
# this may become untenable if more pkgs do that!
$betty.Add("busy-signal")
$betty.Add("intentions")
$betty.Add("linter-ui-default")

$wilma = apm list --no-color --bare --installed
$installed = $wilma.ForEach( { $_.split('@')[0] } )
$differences = Compare-Object -ReferenceObject $installed -DifferenceObject $betty

# Compare-Object returns PSCustomObject if collections are equal (???)
# but is schizo about type of return array
if ($differences.GetType().Name -ne "Object[]" -and $differences.GetType().Name -ne "Array")
{
  Write-Host "There are no differences between installed and" $pkg_list -ForegroundColor Cyan
  exit 0
}

$uninstalled = $differences.Where( { $_.SideIndicator -eq "=>" } )
$uninstalled = $uninstalled.ForEach( { $_.InputObject })
$extra = $differences.Where( { $_.SideIndicator -eq "<=" } )
$extra = $extra.ForEach( { $_.InputObject } )

if ($uninstalled.Count -gt 1 -or $extra[0] -ne "") {
  Write-Host "Packages In $pkg_list Not Installed" -ForegroundColor Red
  $uninstalled.ForEach( { Write-Host $_ })
  Write-Host "`n"
}

if ($extra.Count -gt 1 -or $extra[0] -ne "") {
  Write-Host "Packages Installed But Not in $pkg_list List" -ForegroundColor Red
  $extra.ForEach( { Write-Host $_ })
}

if ($args.Contains("--install")) {
  $uninstalled.ForEach( { apm install --no-color $_ } )
}
