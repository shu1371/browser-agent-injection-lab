$pngDir = 'D:\文章\浏览器Agent注入实战\images\png'
$ud = Get-ChildItem -LiteralPath $pngDir -Directory -Filter 'ud*' -ErrorAction SilentlyContinue
foreach ($d in $ud) {
    Remove-Item -LiteralPath $d.FullName -Recurse -Force
    Write-Output ('REMOVED DIR ' + $d.FullName)
}
