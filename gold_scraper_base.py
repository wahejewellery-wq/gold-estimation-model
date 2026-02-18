import requests
from bs4 import BeautifulSoup
import csv
import re
import json

# ==========================================
# CONFIGURATION SECTION
# ==========================================

# List of Target URLs
URLS = [
    "https://www.wahejewellery.com/products/the-crowned-heart-ring",
    "https://www.wahejewellery.com/products/regalia-prism-princess-ring",
    "https://www.wahejewellery.com/products/celeste-whirl-diamond-ring",
    "https://www.wahejewellery.com/products/imperial-oval-legacy-ring",
    "https://www.wahejewellery.com/products/linea-spark-solitaire-ring",
    "https://www.wahejewellery.com/products/starlace-muse-diamond-ring",
    "https://www.wahejewellery.com/products/majesta-emerald-axis-ring",
    "https://www.wahejewellery.com/products/solar-halo-gold-solitaire",
    "https://www.wahejewellery.com/products/crownbound-promise-ring",
    "https://www.wahejewellery.com/products/lotus-empress-diamond-ring",
    "https://www.wahejewellery.com/products/ovalia-pure-commitment-ring",
    "https://www.wahejewellery.com/products/ironcrest-diamond-band",
    "https://www.wahejewellery.com/products/eternal-verse-bridal-duo",
    "https://www.wahejewellery.com/products/dual-flame-harmony-ring",
    "https://www.wahejewellery.com/products/sterra-light-radiant-ring",
    "https://www.wahejewellery.com/products/veloria-elongated-spark-ring",
    "https://www.wahejewellery.com/products/aurelia-dawn-solitaire-ring",
    "https://www.wahejewellery.com/products/nysa-pearfall-diamond-ring",
    "https://www.wahejewellery.com/products/luminex-radiant-crest-ring",
    "https://www.wahejewellery.com/products/saira-radiant-brilliance-diamond-ring",
    "https://www.wahejewellery.com/products/pure-emerald-cut-eternity-ring",
    "https://www.wahejewellery.com/products/isla-signature-lab-diamond-love-ring",
    "https://www.wahejewellery.com/products/emerald-gleam-lab-diamond-ring",
    "https://www.wahejewellery.com/products/grand-marquise-spark-engagement-ring",
    "https://www.wahejewellery.com/products/timeless-teardrop-lab-diamond-ring",
    "https://www.wahejewellery.com/products/amethyst-royale-princess-diamond-ring",
    "https://www.wahejewellery.com/products/everlasting-heart-lab-diamond-promise-ring",
    "https://www.wahejewellery.com/products/margot-lumiere-lab-diamond-signature-ring",
    "https://www.wahejewellery.com/products/twine-grace-lab-diamond-engagement-ring-9kt",
    "https://www.wahejewellery.com/products/serene-pear-crown-lab-diamond-ring-9kt",
    "https://www.wahejewellery.com/products/heritage-oval-spark-lab-diamond-ring",
    "https://www.wahejewellery.com/products/interlace-luxe-lab-diamond-ring",
    "https://www.wahejewellery.com/products/golden-glow-lab-diamond-statement-ring",
    "https://www.wahejewellery.com/products/lumis-round-lab-diamond-promise-ring",
    "https://www.wahejewellery.com/products/evelyn-oval-brilliance-diamond-ring",
    "https://www.wahejewellery.com/products/celestia-spark-lab-diamond-ring",
    "https://www.wahejewellery.com/products/petaline-radiance-lab-diamond-ring",
    "https://www.wahejewellery.com/products/aurora-circle-lab-diamond-engagement-ring",
    "https://www.wahejewellery.com/products/elegant-promise-diamond-solitaire",
    "https://www.wahejewellery.com/products/statement-pear-diamond-band",
    "https://www.wahejewellery.com/products/signature-1-carat-princess-diamond-ring",
    "https://www.wahejewellery.com/products/heritage-princess-diamond-ring",
    "https://www.wahejewellery.com/products/geometric-asscher-diamond-ring",
    "https://www.wahejewellery.com/products/interlace-brilliance-diamond-ring-1",
    "https://www.wahejewellery.com/products/refined-emerald-solitaire-diamond-ring",
    "https://www.wahejewellery.com/products/pure-harmony-diamond-band",
    "https://www.wahejewellery.com/products/oval-grace-diamond-eternity-band",
    "https://www.wahejewellery.com/products/classic-crown-princess-diamond-ring",
    "https://www.wahejewellery.com/products/versa-luxe-transformable-diamond-ring",
    "https://www.wahejewellery.com/products/ruby-mist-diamond-ring",
    "https://www.wahejewellery.com/products/radiance-flame-gemstone-diamond-ring",
    "https://www.wahejewellery.com/products/scarlet-v-point-ruby-diamond-ring",
    "https://www.wahejewellery.com/products/crimson-rhythm-ruby-diamond-band",
    "https://www.wahejewellery.com/products/three-line-brilliance-diamond-band",
    "https://www.wahejewellery.com/products/midnight-spark-baguette-diamond-ring",
    "https://www.wahejewellery.com/products/framed-princess-cut-diamond-ring",
    "https://www.wahejewellery.com/products/royal-line-baguette-diamond-band",
    "https://www.wahejewellery.com/products/modern-square-cut-diamond-ring-1",
    "https://www.wahejewellery.com/products/celestial-halo-diamond-ring",
    "https://www.wahejewellery.com/products/garden-grace-emerald-diamond-ring",
    "https://www.wahejewellery.com/products/prismatic-pear-cut-diamond-ring",
    "https://www.wahejewellery.com/products/royal-crest-princess-diamond-ring",
    "https://www.wahejewellery.com/products/radiant-love-heart-inspired-diamond-ring",
    "https://www.wahejewellery.com/products/twin-flame-diamond-toi-et-moi-ring",
    "https://www.wahejewellery.com/products/timeless-cushion-elegance-diamond-ring",
    "https://www.wahejewellery.com/products/celestial-arc-diamond-ring",
    "https://www.wahejewellery.com/products/chevron-grace-baguette-diamond-ring",
    "https://www.wahejewellery.com/products/emerald-whirl-statement-diamond-ring",
    "https://www.wahejewellery.com/products/infinity-curve-baguette-diamond-ring",
    "https://www.wahejewellery.com/products/floral-radiance-baguette-diamond-ring",
    "https://www.wahejewellery.com/products/grand-emerald-2-carat-diamond-solitaire",
    "https://www.wahejewellery.com/products/petal-glow-diamond-band",
    "https://www.wahejewellery.com/products/signature-brilliance-heart-arrow-solitaire",
    "https://www.wahejewellery.com/products/blush-drop-pear-shaped-diamond-ring",
    "https://www.wahejewellery.com/products/majestic-emerald-cut-solitaire-ring",
    "https://www.wahejewellery.com/products/radiant-stack-diamond-eternity-band",
    "https://www.wahejewellery.com/products/luminous-three-stone-diamond-ring",
    "https://www.wahejewellery.com/products/heritage-halo-vintage-diamond-ring",
    "https://www.wahejewellery.com/products/eternal-trinity-lab-diamond-ring",
    "https://www.wahejewellery.com/products/regal-aura-princess-diamond-ring",
    "https://www.wahejewellery.com/products/opulence-mosaic-cocktail-ring",
    "https://www.wahejewellery.com/products/imperial-chestnut-diamond-ring",
    "https://www.wahejewellery.com/products/harmonia-diamond-symphony-ring",
    "https://www.wahejewellery.com/products/majestic-radiant-crown-ring",
    "https://www.wahejewellery.com/products/marquise-ribbon-infinity-ring",
    "https://www.wahejewellery.com/products/pearlflare-solitaire-ring",
    "https://www.wahejewellery.com/products/radiance-eternal-diamond-ring",
    "https://www.wahejewellery.com/products/halo-crest-engagement-ring",
    "https://www.wahejewellery.com/products/regal-emerald-continuum-band",
    "https://www.wahejewellery.com/products/amour-spark-engagement-ring",
    "https://www.wahejewellery.com/products/emerald-reverie-diamond-ring",
    "https://www.wahejewellery.com/products/gilded-emerald-heirloom-ring",
    "https://www.wahejewellery.com/products/infinity-grace-diamond-ring",
    "https://www.wahejewellery.com/products/solara-radiant-promise-ring",
    "https://www.wahejewellery.com/products/antique-whisper-diamond-ring",
    "https://www.wahejewellery.com/products/muse-elan-diamond-ring",
    "https://www.wahejewellery.com/products/radiant-fivefold-solitaire-ring",
    "https://www.wahejewellery.com/products/nova-helix-diamond-ring",
    "https://www.wahejewellery.com/products/heritage-trinity-emerald-ring",
    "https://www.wahejewellery.com/products/eternal-ember-marquise-ring",
    "https://www.wahejewellery.com/products/luna-crest-bridal-diamond-ring",
    "https://www.wahejewellery.com/products/aurelia-promise-ring",
    "https://www.wahejewellery.com/products/verdant-arc-diamond-band",
    "https://www.wahejewellery.com/products/celeste-flow-diamond-ring",
    "https://www.wahejewellery.com/products/ready-radiance-lab-grown-diamond-ring",
    "https://www.wahejewellery.com/products/eternal-trinity-lab-grown-diamond-bridal-ring",
    "https://www.wahejewellery.com/products/ivory-halo-lab-grown-diamond-cluster-band",
    "https://www.wahejewellery.com/products/trinity-luxe-lab-grown-diamond-cocktail-ring",
    "https://www.wahejewellery.com/products/silken-loop-lab-grown-diamond-ring",
    "https://www.wahejewellery.com/products/astra-hexa-lab-grown-diamond-engagement-ring",
    "https://www.wahejewellery.com/products/amethyst-glow-lab-grown-diamond-ring",
    "https://www.wahejewellery.com/products/imperial-radiance-2-ct-lab-grown-diamond-engagement-ring",
    "https://www.wahejewellery.com/products/forever-promise-lab-grown-diamond-solitaire-ring",
    "https://www.wahejewellery.com/products/elysia-pear-lab-grown-diamond-solitaire-ring",
    "https://www.wahejewellery.com/products/valen-lab-grown-diamond-classic-ring",
    "https://www.wahejewellery.com/products/aurora-oval-lab-grown-diamond-solitaire-ring",
    "https://www.wahejewellery.com/products/celestial-bloom-lab-grown-diamond-cocktail-ring",
    "https://www.wahejewellery.com/products/eternal-crest-lab-grown-diamond-band",
    "https://www.wahejewellery.com/products/arden-lab-grown-diamond-statement-ring",
    "https://www.wahejewellery.com/products/heirloom-grace-marquise-lab-grown-diamond-bridal-ring",
    "https://www.wahejewellery.com/products/heritage-halo-vintage-diamond-ring",
    "https://www.wahejewellery.com/products/eternal-trinity-lab-diamond-ring",
    "https://www.wahejewellery.com/products/regal-aura-princess-diamond-ring",
    "https://www.wahejewellery.com/products/harmonia-diamond-symphony-ring",
    "https://www.wahejewellery.com/products/majestic-radiant-crown-ring",
    "https://www.wahejewellery.com/products/evermore-oval-cluster-diamond-engagement-ring",
    "https://www.wahejewellery.com/products/timeless-grace-lab-grown-diamond-solitaire-band",
    "https://www.wahejewellery.com/products/mosaic-aura-band",
    "https://www.wahejewellery.com/products/galaxia-spark-cocktail-ring",
    "https://www.wahejewellery.com/products/half-peak-sleek-ring",
    "https://www.wahejewellery.com/products/harmonia-field-diamond-ring",
    "https://www.wahejewellery.com/products/ariaguard-promise-solitaire",
    "https://www.wahejewellery.com/products/lightbound-infinity-ring",
    "https://www.wahejewellery.com/products/elysian-majesty-diamond-ring",
    "https://www.wahejewellery.com/products/forever-embrace-oval-solitaire-ring",
    "https://www.wahejewellery.com/products/pure-radiance-liora-ring",
    "https://www.wahejewellery.com/products/oval-harmony-radiance-ring",
    "https://www.wahejewellery.com/products/triluxe-embrace-diamond-ring",
    "https://www.wahejewellery.com/products/vellatwist-round-lab-diamond-ring",
    "https://www.wahejewellery.com/products/cushion-radiance-side-stone-ring",
    "https://www.wahejewellery.com/products/sidenity-oval-cut-sides-stone-lab-diamond-ring",
    "https://www.wahejewellery.com/products/crownaura-pave-baguette-band",
    "https://www.wahejewellery.com/products/bezel-brilliance-emerald-baguette-band",
    "https://www.wahejewellery.com/products/shinebound-diamond-ring",
    "https://www.wahejewellery.com/products/brilliance-trail-diamond-ring",
    "https://www.wahejewellery.com/products/devoted-heart-diamond-ring",
    "https://www.wahejewellery.com/products/eternachannel-diamond-ring",
    "https://www.wahejewellery.com/products/round-radiance-eternity-band",
    "https://www.wahejewellery.com/products/oval-pave-bypass-elegance-ring",
    "https://www.wahejewellery.com/products/twin-radiance-emerald-ring",
    "https://www.wahejewellery.com/products/divine-crest-crown-ring",
    "https://www.wahejewellery.com/products/eternapear-classic-diamond-ring",
    "https://www.wahejewellery.com/products/crownlight-classic-round-diamond-ring",
    "https://www.wahejewellery.com/products/halo-amora-heart-ring",
    "https://www.wahejewellery.com/products/twistluxe-round-side-stone-ring",
    "https://www.wahejewellery.com/products/emerald-cascade-eternity-band",
    "https://www.wahejewellery.com/products/pureluxe-round-solitaire-lab-diamond-ring",
    "https://www.wahejewellery.com/products/renahalo-round-cut-diamond-ring",
    "https://www.wahejewellery.com/products/aurevara-round-halo-lab-diamond-ring",
    "https://www.wahejewellery.com/products/graceline-emerald-halo-ring",
    "https://www.wahejewellery.com/products/auraleen-split-shank-oval-halo-ring",
    "https://www.wahejewellery.com/products/oval-affinity-halo-diamond-ring",
    "https://www.wahejewellery.com/products/celestia-heart-radiance-band",
    "https://www.wahejewellery.com/products/florea-lumiere-diamond-ring",
    "https://www.wahejewellery.com/products/eterna-amor-half-eternity-ring",
    "https://www.wahejewellery.com/products/celestia-twin-oval-promise-set",
    "https://www.wahejewellery.com/products/virelle-ascend-diamond-ring",
    "https://www.wahejewellery.com/products/blossom-elan-diamond-ring",
    "https://www.wahejewellery.com/products/celestia-emerald-cut-eternity-ring",
    "https://www.wahejewellery.com/products/mosaic-brilliance-diamond-ring",
    "https://www.wahejewellery.com/products/interlace-brilliance-diamond-ring",
    "https://www.wahejewellery.com/products/eterna-duo-diamond-flow-ring",
    "https://www.wahejewellery.com/products/aurora-marquise-halo-diamond-ring",
    "https://www.wahejewellery.com/products/amoura-dual-cut-open-diamond-ring",
    "https://www.wahejewellery.com/products/luminara-radiant-eternity-band",
    "https://www.wahejewellery.com/products/amora-heart-solitaire-diamond-ring-copy",
    "https://www.wahejewellery.com/products/titan-crest-solitaire-ring-copy",
    "https://www.wahejewellery.com/products/the-trinity-horizon-ring",
    "https://www.wahejewellery.com/products/the-royal-heart-ring",
    "https://www.wahejewellery.com/products/the-serene-swirl-ring",
    "https://www.wahejewellery.com/products/the-sweet-bowknot-ring",
    "https://www.wahejewellery.com/products/the-flight-of-fancy-ring",
    "https://www.wahejewellery.com/products/the-gardenia-sparkle-ring",
    "https://www.wahejewellery.com/products/the-forever-eternity-band",
    "https://www.wahejewellery.com/products/the-embrace-contour-ring",
    "https://www.wahejewellery.com/products/the-intertwined-love-ring",
    "https://www.wahejewellery.com/products/diamond-swirl-ring",
    "https://www.wahejewellery.com/products/infinity-curve-diamond-ring",
    "https://www.wahejewellery.com/products/the-teardrop-diamond-band-ring",
    "https://www.wahejewellery.com/products/the-diamond-wide-row-band-ring",
    "https://www.wahejewellery.com/products/the-sapphire-cocktail-ring",
    "https://www.wahejewellery.com/products/the-emerald-and-diamond-cocktail-ring",
    "https://www.wahejewellery.com/products/the-crossover-diamond-ring",
    "https://www.wahejewellery.com/products/the-wide-eternity-band-ring",
    "https://www.wahejewellery.com/products/the-curving-diamond-ring",
    "https://www.wahejewellery.com/products/the-aurora-flare-cocktail-ring",
    "https://www.wahejewellery.com/products/the-scalloped-diamond-band-ring",
    "https://www.wahejewellery.com/products/nova-grace-band",
    "https://www.wahejewellery.com/products/embrace-heart-ring",
    "https://www.wahejewellery.com/products/elysia-marquise-bloom-diamond-ring",
    "https://www.wahejewellery.com/products/regal-bloom-emerald-diamond-statement-ring",
    "https://www.wahejewellery.com/products/whispering-leaves-diamond-statement-ring",
    "https://www.wahejewellery.com/products/paramount-solitaire-diamond-ring",
    "https://www.wahejewellery.com/products/the-sovereign-solitaire-diamond-ring",
    "https://www.wahejewellery.com/products/trevalon-2ct-tapred-baguettes-oval-cut-three-stone-ring",
    "https://www.wahejewellery.com/products/serena-teardrop-glow-ring",
    "https://www.wahejewellery.com/products/halo-engagement-ring-with-brightband",
    "https://www.wahejewellery.com/products/seraphina-oval-bloom-ring",
    "https://www.wahejewellery.com/products/solondelle-1-50ct-oval-cut-solitaire-ring",
    "https://www.wahejewellery.com/products/apex-solitaire-diamond-ring",
    "https://www.wahejewellery.com/products/celestia-framed-elegance-ring",
    "https://www.wahejewellery.com/products/aurora-dual-stone-designer-ring",
    "https://www.wahejewellery.com/products/marquessa-heartline-ring",
    "https://www.wahejewellery.com/products/delioraia-split-shank-round-cut-delicate-lab-diamond-ring",
    "https://www.wahejewellery.com/products/enchanted-vine-diamond-ring",
    "https://www.wahejewellery.com/products/aurum-marquise-pear-diamond-crossover-ring",
    "https://www.wahejewellery.com/products/regalia-pearfall-diamond-earrings",
    "https://www.wahejewellery.com/products/cascade-brilliance-diamond-drop-earrings",
    "https://www.wahejewellery.com/products/modern-link-pear-emerald-lab-diamond-earrings",
    "https://www.wahejewellery.com/products/opaline-bloom-lab-diamond-earrings",
    "https://www.wahejewellery.com/products/papillon-verde-emerald-lab-diamond-earrings",
    "https://www.wahejewellery.com/products/rose-petal-radiance-lab-diamond-earrings",
    "https://www.wahejewellery.com/products/linear-glow-danglers",
    "https://www.wahejewellery.com/products/bow-delight-earrings",
    "https://www.wahejewellery.com/products/superior-spark-earrings",
    "https://www.wahejewellery.com/products/circul-charm-earrings",
    "https://www.wahejewellery.com/products/aira-elegance-drops",
    "https://www.wahejewellery.com/products/flutter-diamond-studs",
    "https://www.wahejewellery.com/products/royal-2-carat-solitaire-studs",
    "https://www.wahejewellery.com/products/epure-cushion-dangle-earrings",
    "https://www.wahejewellery.com/products/open-teardrop-diamond-earrings",
    "https://www.wahejewellery.com/products/marquise-vine-huggie-earrings",
    "https://www.wahejewellery.com/products/contemporary-diamond-vine-earrings",
    "https://www.wahejewellery.com/products/layered-diamond-stud-earrings",
    "https://www.wahejewellery.com/products/contemporary-diamond-leaf-earrings",
    "https://www.wahejewellery.com/products/halo-oval-dangle-earrings",
    "https://www.wahejewellery.com/products/floral-halo-stud-earrings",
    "https://www.wahejewellery.com/products/diamond-halo-studs",
    "https://www.wahejewellery.com/products/halo-heart-drop-diamond-studs",
    "https://www.wahejewellery.com/products/diamond-flare-stud-earrings",
    "https://www.wahejewellery.com/products/pear-halo-leverback-drop-earrings",
    "https://www.wahejewellery.com/products/vertical-diamond-dangler-earrings",
    "https://www.wahejewellery.com/products/diamond-halo-cluster-studs",
    "https://www.wahejewellery.com/products/floating-diamond-circle-stud-earrings",
    "https://www.wahejewellery.com/products/knife-edge-huggie-hoop-earrings",
    "https://www.wahejewellery.com/products/graduated-five-stone-diamond-huggie-earrings",
    "https://www.wahejewellery.com/products/the-tender-heart-studs",
    "https://www.wahejewellery.com/products/the-pear-drop-dazzle-hoops",
    "https://www.wahejewellery.com/products/the-convertible-drop-earrings",
    "https://www.wahejewellery.com/products/petal-drop-earrings",
    "https://www.wahejewellery.com/products/eternal-bow-diamond-earrings",
    "https://www.wahejewellery.com/products/0-5ct-oval-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/0-5ct-round-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/1ct-round-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/1ct-marquise-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/1ct-pear-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/1-00ct-round-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/1ct-pear-shape-fancy-studs-earrings",
    "https://www.wahejewellery.com/products/1ct-round-shape-fancy-studs-earrings",
    "https://www.wahejewellery.com/products/1-5ct-round-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/1-75ct-emerald-shape-halo-studs-earrings",
    "https://www.wahejewellery.com/products/2ct-heart-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/1-5ct-round-shape-fancy-studs-earrings",
    "https://www.wahejewellery.com/products/2-5ct-round-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/3ct-round-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/2-50ct-round-shape-halo-studs",
    "https://www.wahejewellery.com/products/4-5ct-emerald-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/5ct-emerald-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/7-00ct-round-shape-solitaire-studs-earrings",
    "https://www.wahejewellery.com/products/1-5ct-pear-shape-dangles-earrings",
    "https://www.wahejewellery.com/products/0-75ct-pear-shape-dangles-earrings",
    "https://www.wahejewellery.com/products/1-25ct-marquise-shape-dangles-earrings",
    "https://www.wahejewellery.com/products/aurora-flare-earrings",
    "https://www.wahejewellery.com/products/3ct-round-shape-dangles-earrings",
    "https://www.wahejewellery.com/products/5-5ct-pear-shape-dangles-earrings",
    "https://www.wahejewellery.com/products/2ct-round-shape-dangles-earrings",
    "https://www.wahejewellery.com/products/3ct-round-shape-fancy-studs-earrings",
    "https://www.wahejewellery.com/products/diamond-ruby-red-drop-dangle-earrings",
    "https://www.wahejewellery.com/products/round-halo-dangled-drop-earrings",
    "https://www.wahejewellery.com/products/cushion-halo-diamond-stud-earrings",
    "https://www.wahejewellery.com/products/pearluxe-halo-diamond-stud-earrings",
    "https://www.wahejewellery.com/products/radiant-elegant-huggie-hoop-earrings",
    "https://www.wahejewellery.com/products/teardrop-diamond-dangle-earrings",
    "https://www.wahejewellery.com/products/elegant-pear-cut-diamond-earrings",
    "https://www.wahejewellery.com/products/vega-sleek-hoop-earrings",
    "https://www.wahejewellery.com/products/gemini-gleam-toi-et-moi-stud-earrings",
    "https://www.wahejewellery.com/products/linea-luxe-lab-diamond-station-necklace",
    "https://www.wahejewellery.com/products/aurelia-grace-lab-diamond-necklace",
    "https://www.wahejewellery.com/products/twin-soul-diamond-necklace",
    "https://www.wahejewellery.com/products/janelle-signature-diamond-necklace",
    "https://www.wahejewellery.com/products/fluid-arc-diamond-necklace",
    "https://www.wahejewellery.com/products/interlace-hearts-arrows-diamond-necklace",
    "https://www.wahejewellery.com/products/infinity-bond-diamond-necklace",
    "https://www.wahejewellery.com/products/prism-form-geometric-diamond-necklace",
    "https://www.wahejewellery.com/products/minimal-radiance-diamond-necklace",
    "https://www.wahejewellery.com/products/lustre-pearl-diamond-embrace-necklace",
    "https://www.wahejewellery.com/products/ethereal-wing-diamond-necklace",
    "https://www.wahejewellery.com/products/verdant-dew-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/vertex-v-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/infinite-amour-diamond-necklace",
    "https://www.wahejewellery.com/products/isla-swirl-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/flora-drift-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/noctis-gleam-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/amora-pure-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/aureon-crown-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/circa-glow-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/velora-line-lab-grown-diamond-necklace",
    "https://www.wahejewellery.com/products/elonge-luxe-y-chain-necklace",
    "https://www.wahejewellery.com/products/nova-circle-trinity-necklace",
    "https://www.wahejewellery.com/products/axis-modern-square-necklace",
    "https://www.wahejewellery.com/products/fusion-cut-diamond-necklace",
    "https://www.wahejewellery.com/products/twin-radiance-solitaire-necklace",
    "https://www.wahejewellery.com/products/asyme-spark-linear-necklace",
    "https://www.wahejewellery.com/products/eterna-grace-loop-necklace",
    "https://www.wahejewellery.com/products/aurelle-classic-solitaire-necklace",
    "https://www.wahejewellery.com/products/celestia-petal-diamond-necklace",
    "https://www.wahejewellery.com/products/midnight-constellation-diamond-necklace",
    "https://www.wahejewellery.com/products/petite-nova-diamond-necklace",
    "https://www.wahejewellery.com/products/asym-glow-solitaire-necklace",
    "https://www.wahejewellery.com/products/elara-layered-shine-necklace",
    "https://www.wahejewellery.com/products/radiant-beam-diamond-necklace",
    "https://www.wahejewellery.com/products/ovaluxe-pure-glow-necklace",
    "https://www.wahejewellery.com/products/twin-flame-diamond-harmony-necklace",
    "https://www.wahejewellery.com/products/ziora-minimal-spark-necklace",
    "https://www.wahejewellery.com/products/architect-cut-diamond-heirloom-necklace",
    "https://www.wahejewellery.com/products/dual-soul-diamond-embrace-necklace",
    "https://www.wahejewellery.com/products/luna-arc-diamond-necklace",
    "https://www.wahejewellery.com/products/stellar-line-diamond-necklace",
    "https://www.wahejewellery.com/products/regalia-drop-diamond-necklace",
    "https://www.wahejewellery.com/products/icy-vine-lumina-necklace",
    "https://www.wahejewellery.com/products/bloomfall-diamond-grace-necklace",
    "https://www.wahejewellery.com/products/halo-drift-elegance-necklace",
    "https://www.wahejewellery.com/products/veya-trinity-glow-diamond-necklace",
    "https://www.wahejewellery.com/products/aurelle-classic-radiance-necklace",
    "https://www.wahejewellery.com/products/luminara-grand-brilliance-necklace",
    "https://www.wahejewellery.com/products/celestia-one-spark-diamond-necklace",
    "https://www.wahejewellery.com/products/art-deco-diamond-drop-pendant-necklace",
    "https://www.wahejewellery.com/products/diamond-infinity-swirl-pendant-necklace",
    "https://www.wahejewellery.com/products/geometric-diamond-solitaire-drop-necklace",
    "https://www.wahejewellery.com/products/the-classic-halo-solitaire-diamond-layered-necklace",
    "https://www.wahejewellery.com/products/the-round-playing-lariat-necklace",
    "https://www.wahejewellery.com/products/the-diamond-arc-layered-necklace",
    "https://www.wahejewellery.com/products/the-dangling-diamond-layered-chain-necklace",
    "https://www.wahejewellery.com/products/grace-diamond-lariat-necklace",
    "https://www.wahejewellery.com/products/radiant-bloom-diamond-necklace",
    "https://www.wahejewellery.com/products/eternal-bow-diamond-necklace",
    "https://www.wahejewellery.com/products/timeless-aura-diamond-tennis-necklace",
    "https://www.wahejewellery.com/products/radiant-elegance-bar-necklace",
    "https://www.wahejewellery.com/products/eterna-spark-lab-diamond-line-bracelet",
    "https://www.wahejewellery.com/products/verdant-crown-emerald-lab-diamond-bracelet",
    "https://www.wahejewellery.com/products/lunadrop-bezel-pear-lab-diamond-bracelet",
    "https://www.wahejewellery.com/products/heritage-emerald-cut-lab-diamond-bracelet",
    "https://www.wahejewellery.com/products/diamond-blossom-bangle",
    "https://www.wahejewellery.com/products/hollywood-glam-tennis-bracelet",
    "https://www.wahejewellery.com/products/magical-mirage-bangle",
    "https://www.wahejewellery.com/products/blooming-diamond-bangle",
    "https://www.wahejewellery.com/products/grand-luxe-brilliant-bracelet",
    "https://www.wahejewellery.com/products/heritage-ridge-bracelet",
    "https://www.wahejewellery.com/products/minimal-solitaire-diamond-bracelet",
    "https://www.wahejewellery.com/products/the-mixed-cut-diamond-tennis-bracelet",
    "https://www.wahejewellery.com/products/the-tripple-halo-chain-bracelet",
    "https://www.wahejewellery.com/products/the-playing-chain-solitaire-diamond-bracelet",
    "https://www.wahejewellery.com/products/the-dangling-diamond-chain-bracelet",
    "https://www.wahejewellery.com/products/lumina-eternity-bracelet",
    "https://www.wahejewellery.com/products/lunar-glow-diamond-bangle",
    "https://www.wahejewellery.com/products/double-row-diamond-bracelet",
    "https://www.wahejewellery.com/products/seraphic-spark-diamond-bangle",
    "https://www.wahejewellery.com/products/eternal-bloom-diamond-bracelet",
    "https://www.wahejewellery.com/products/touch-of-sophistication-classy-stiff-oval-bangle",
    "https://www.wahejewellery.com/products/timeless-elegance-eternal-spark-diamond-bangle",
    "https://www.wahejewellery.com/products/exquisite-bezel-tennis-bracelet",
    "https://www.wahejewellery.com/products/eternal-grace-diamond-bracelet",
    "https://www.wahejewellery.com/products/stunning-3-prong-round-tennis-bracelet"
]


# CSS SELECTORS
SELECTORS = {
    "price_table": "#full_description table",
    "image_meta": "meta[property='og:image']",
    "image_fallback": ".product-main-image img",
    "title": "h1.product-single__title", # Title often contains category
    "breadcrumb": ".breadcrumb a, .breadcrumbs a", # fallback for category
}

# Output filename
CSV_FILENAME = "gold_data.csv"

# ==========================================
# SCRAPING LOGIC
# ==========================================

def get_soup(url):
    """Fetches the URL and returns a BeautifulSoup object."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def clean_text(text):
    if text:
        return text.strip().replace('\n', ' ').replace('\r', '')
    return "N/A"

def extract_weight_value(text):
    if not text:
        return "N/A"
    match = re.search(r'(\d+(\.\d*)?)\s*([a-zA-Z]+)', text)
    if match:
        return match.group(0)
    return text

def extract_category(soup):
    """Extracts product category from metadata or title."""
    # 1. Try to find 'type' in Shopify Javascript object
    # heavily dependent on page structure, but often present in script tags
    # looking for: "product": { ... "type": "Ring" ... }
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and '"type":' in script.string and '"product":' in script.string:
            # simple regex to find "type":"Value" close to "product"
            # This is brittle but can work without JS engine
            match = re.search(r'"type"\s*:\s*"([^"]+)"', script.string)
            if match:
                return match.group(1)
            
    # 2. Try Title (Last word usually is category, e.g. "Diamond Ring" -> "Ring")
    title_elem = soup.select_one(SELECTORS["title"])
    if title_elem:
        title_text = clean_text(title_elem.text)
        # simplistic: just take the last word
        if title_text:
            return title_text.split()[-1]

    return "N/A"

def scrape_single_url(url):
    soup = get_soup(url)
    if not soup:
        return []

    results = []
    
    # Extract Basic Details
    category = extract_category(soup)
    
    image_link = "N/A"
    img_meta = soup.select_one(SELECTORS["image_meta"])
    if img_meta and img_meta.get("content"):
        image_link = img_meta["content"]
    else:
        img_elem = soup.select_one(SELECTORS["image_fallback"])
        if img_elem:
           image_link = img_elem.get("src") or img_elem.get("data-src") or "N/A"
    
    if image_link and image_link.startswith("//"):
        image_link = "https:" + image_link

    # Locate the Price Breakup Table
    table = soup.select_one(SELECTORS["price_table"])
    
    if not table:
        print(f"[{url}] Could not find Price Breakup table.")
        return []

    # Parse headers
    headers = [th.get_text(strip=True) for th in table.select("thead tr th")]
    if not headers:
        headers = [td.get_text(strip=True) for td in table.select("thead tr td")]
    
    purity_indices = {} 
    for idx, header in enumerate(headers):
        if "KT" in header.upper() or "K" in header.upper(): 
             purity_indices[idx] = header

    gold_weights = {} 
    diamond_weight = "N/A"

    rows = table.select("tbody tr")
    for row in rows:
        cells = row.select("td")
        if not cells: 
            continue
        
        row_label = clean_text(cells[0].get_text())
        
        if "Gold Weight" in row_label:
            for idx, purity in purity_indices.items():
                if idx < len(cells):
                    weight = clean_text(cells[idx].get_text())
                    gold_weights[purity] = weight
        
        if "Diamond" in row_label:
            match = re.search(r'\(?(\d+(\.\d*)?)\s*ct\)?', row_label, re.IGNORECASE)
            if match:
                diamond_weight = match.group(1) + " ct"

    # Create entries
    if gold_weights:
        for purity, weight in gold_weights.items():
            item = {
                "Category": category,
                "Gold Purity": purity,
                "Gold Weight": weight,
                "Image Link": image_link,
                "Diamond Weight": diamond_weight,
                "Product URL": url # Succesfully tracking source URL
            }
            results.append(item)
    
    return results

def scrape_all():
    all_data = []
    for url in URLS:
        print(f"Scraping: {url}")
        data = scrape_single_url(url)
        all_data.extend(data)
    return all_data

def save_to_csv(data, filename):
    if not data:
        print("No data extracted.")
        return

    fieldnames = ["Category", "Gold Purity", "Gold Weight", "Image Link", "Diamond Weight", "Product URL"]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully saved data to {filename}")
    except IOError as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    print("Starting batch scraper...")
    data = scrape_all()
    save_to_csv(data, CSV_FILENAME)
