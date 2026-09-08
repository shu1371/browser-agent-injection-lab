$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$img = 'D:\文章\浏览器Agent注入实战\images'
New-Item -ItemType Directory -Force -Path (Join-Path $img 'png') | Out-Null
$items = @(
    @{ svg = 'fig1_architecture.svg'; png = 'fig1_architecture.png'; ud = 'ud1' },
    @{ svg = 'fig2_attack_chain.svg'; png = 'fig2_attack_chain.png'; ud = 'ud2' },
    @{ svg = 'fig3_defense.svg'; png = 'fig3_defense.png'; ud = 'ud3' },
    @{ svg = 'fig4_results.svg'; png = 'fig4_results.png'; ud = 'ud4' }
)
foreach ($j in $items) {
    $svgFile = Join-Path $img $j.svg
    $src = [System.Uri]::new($svgFile).AbsoluteUri
    $shot = Join-Path (Join-Path $img 'png') $j.png
    $ud = Join-Path (Join-Path $img 'png') $j.ud
    & $edge --headless=new --disable-gpu --user-data-dir=$ud --force-device-scale-factor=2 --window-size=1280,860 --screenshot=$shot $src 2>$null
    Start-Sleep -Seconds 3
}
Get-ChildItem -LiteralPath (Join-Path $img 'png') -Filter '*.png' | Select-Object Name, Length
