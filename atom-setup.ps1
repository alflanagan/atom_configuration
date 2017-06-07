# for node-gyp
$env:PYTHON = "C:\Python27\pythonw.exe"
$pkg_list = "my-packages.txt"
if ($env:OS -Like "Windows*")
{
    $pkg_list = "my-windows-packages.txt"
}

$DEPENDENCIES = @{linter = @("linter-ui-default");
                  "linter-ui-default" = @("intentions", "busy-signal");
                  "pythonic-atom" = @("linter", "linter-ui-default", "linter-pycodestyle", "minimap",
                                  "minimap-linter", "MagicPython", "python-tools", "python-yapf",
                                  "autocomplete-python", "hyperclick", "script", "python-isort")
               }

$expected = New-Object System.Collections.Generic.List[System.Object]
(Get-Content $pkg_list).ForEach( { $expected.Add($_) } )
# add auto-installed dependent pkgs
$DEPENDENCIES.Keys.ForEach({$DEPENDENCIES[$_].ForEach({$expected.Add($_)})})

$wilma = apm list --no-color --bare --installed
$installed = $wilma.ForEach( { $_.split('@')[0] } )
$differences = Compare-Object -ReferenceObject $installed -DifferenceObject $expected

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
