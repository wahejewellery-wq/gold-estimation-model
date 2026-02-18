import requests
from bs4 import BeautifulSoup
import json
import re
import csv
import os

# Target URLs
URLS = [
    "https://geer.in/products/2-5ct-round-shape-gold-chain-bracelets/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/alura-8ct-shared-prong-round-tennis-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/brilliant-round-delicate-gold-ring-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/arista-8-75ct-oval-cut-tennis-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/athena-greek-key-diamond-bangle/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/bangle-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/celeste-diamond-embellished-bangles-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/odelia-21-25ct-alternative-setting-fancy-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/contemporary-dual-row-sparkling-bangle-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/eterna-spark-bangle-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/celeste-spark-bangle/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/brina-fancy-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/contemporary-dual-row-sparkling-bangle/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/dazzling-love-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/divine-luster-single-heart-stone-delicate-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/elegant-floral-gemstone-and-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/elegant-red-stone-halo-gold-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/emerald-cut-lab-grown-diamond-chain-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/emerald-radiance-link-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lustrous-illusion-bangles-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/faela-2ct-round-cut-double-chain-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/zenith-9-75ct-cushion-cut-tennis-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/floral-bloom-open-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/serene-linea-bangle-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/isara-3-5ct-shared-prong-round-cut-tennis-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/celia-5ct-floral-round-cut-fancy-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lavina-1-75ct-single-round-cut-kada-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/leaf-whisper-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/luminous-marquise-round-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/regal-radiance-diamond-bangle-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lustre-line-bangle-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/sidenaire-4ct-standard-emerald-cut-side-stone-ring-copy-2/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/nessa-2-25ct-criss-cross-oval-cut-kada-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/nydia-1-25ct-two-unique-cut-kada-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/vira-5-75ct-contemporary-fancy-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/radiant-bow-charm-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/regal-radiance-diamond-bangle/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/serena-grande-statement-bangle/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/celeste-spark-bangle-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/evelia-double-round-cut-link-chain-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/anise-2ct-leaf-style-round-cut-kada-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/odelia-21-25ct-alternative-setting-fancy-bracelet-copy-1/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/viera-pear-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/emerald-cut-lab-grown-diamond-chain-bracelet-copy-1/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/vellina-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/zia-alternative-setting-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/halcyon-floral-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lira-bar-setting-round-cut-kada-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/virelle-round-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/nivara-emerald-cut-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/maris-bezel-set-emerald-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/maren-round-cut-chain-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/ilara-alternative-setting-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/zeira-emerald-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/celina-beaded-round-cut-kada-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/elysia-bezel-setting-emerald-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/calista-consistent-setting-oval-cut-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/elara-round-cut-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/niva-infinity-round-cut-kada-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/freya-adjustable-round-cut-kada-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/viera-pear-cut-fancy-lab-diamond-bracelet-1/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/aisla-round-cut-gauge-wire-chain-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/amara-bezel-set-emerald-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/oriel-marquise-wave-style-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/irena-shared-setting-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/avari-shared-setting-oval-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/oria-floral-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/neva-shared-prong-round-cut-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/auroria-princess-cut-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/opalora-single-pear-cut-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/delara-standard-round-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/nixie-6ct-emerald-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/brio-three-row-round-cut-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/isola-emerald-cut-link-chain-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/tivara-floating-marquise-cut-tennis-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/kaela-bezel-setting-round-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/sia-unstable-round-cut-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/galya-2two-row-pear-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/naida-contemporary-style-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/elyse-two-row-pear-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/calyx-alternative-two-row-round-cut-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/solis-two-row-marquise-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/mylia-three-row-emerald-cut-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/infinity-charm-emerald-cut-delicate-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/vesper-marquise-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lina-flower-style-pear-cut-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/vion-alternative-two-row-round-cut-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/marisca-bezel-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/silara-miracle-setting-oval-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/avelis-double-emerald-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/alera-bezel-set-2stone-kada-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/opulent-mosaic-multi-cut-diamond-statement-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/vera-wave-round-cut-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/diamond-aura-three-unique-shape-delicate-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/novella-double-row-round-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/aelina-bloom-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/fionna-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/infinite-sparkle-open-diamond-bracele-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lysandra-oval-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/aurora-belle-falling-round-cut-delicate-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/starlight-path-diamond-bangle-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/evra-miracle-setting-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/orin-emerald-cut-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/fael-fancy-lab-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/precision-pave-square-diamond-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/orbital-sparkle-diamond-link-bracelet-copy/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/viora-1-50ct-miracle-setting-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/delistreve-split-shank-round-cut-delicate-lab-diamond-ring-1/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/mirae-2-50ct-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/eira-3ct-four-row-radiant-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/regal-three-prong-open-heart-delicate-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/orla-split-emerald-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/cassia-1-75ct-emerald-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/amelina-4-25ct-emerald-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/caelis-8ct-marquise-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/valen-1-50ct-cushion-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/melis-1-50ct-split-shank-marquise-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lumis-2ct-oval-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/avira-2-75ct-split-emerald-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/sienna-3-75ct-marquise-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/rinna-3-75ct-shared-setting-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/astra-6ct-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/vivara-4-5ct-standard-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/nyssa-heart-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/anya-3-25ct-studded-round-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lumin-3-75ct-round-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/celara-bezel-heart-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/ivory-diamond-round-cut-delicate-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/daria-split-shank-emerald-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/calia-double-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/zaira-1-5ct-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/rivara-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/fiara-11-5ct-shared-prong-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/bria-2ct-leafy-whisper-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/miri-1-25ct-two-row-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/marelle-10-5ct-two-row-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/alora-2ct-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/mira-surface-round-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/atria-6-75ct-miracle-setting-marquise-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/vellia-0-50ct-single-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/livia-1-25ct-bezel-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/eterna-shine-3-25ct-bezel-setting-round-cut-delicate-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/ilyra-loop-round-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/ravina-oval-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/arelis-3-75ct-bypass-pear-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lumina-charm-round-cut-delicate-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/thalia-2-5ct-miracle-setting-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/fara-13-25ct-miracle-setting-emerald-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/aeliana-3ct-split-oval-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/eirlys-8ct-shared-prong-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/alina-3ct-reversed-tapred-oval-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/elara-2ct-split-oval-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/lyra-5ct-oval-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/melora-oval-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/zaria-4-25ct-split-oval-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/briona-oval-cut-kada-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/riona-6ct-sterling-round-cut-tennis-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/tyra-cushion-cut-fancy-lab-diamond-bracelet/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/aurora-luxe-diamond-bangle/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/celeste-sparkle-diamond-bangle/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/elysian-halo-diamond-bangle/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/eternal-love-diamond-kada/from_collection=lab-grown-diamonds-bracelets-and-bangles",
    "https://geer.in/products/1-5ct-round-shape-solitaire-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-5ct-round-shape-delicate-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/eternal-glow-round-shape-delicate-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-75ct-round-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-princess-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-5ct-round-shape-solitaire-studs-earrings-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-solitaire-studs-earrings-2/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-5ct-round-shape-fancy-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-50ct-pear-shape-fancy-stud/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/5-5ct-pear-shape-dangles-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-25ct-round-shape-halo-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-25ct-oval-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-25ct-round-shape-halo-studs-earrings-copy-2/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-pear-shape-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-75ct-pear-shape-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-asscher-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-25ct-round-shape-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-solitaire-studs-earrings-3/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/luxe-links-round-shape-delicate-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-75ct-pear-shape-solitaire-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-pear-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-25ct-round-cut-halo-stud-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-5ct-dazzle-dangle-earrings-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-75ct-emerald-shape-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-00ct-round-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-5ct-round-shape-delicate-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-5ct-pear-shape-dangles-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-50ct-round-shape-hoops-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-50ct-round-shape-fancy-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-25ct-round-shape-halo-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-5ct-round-shape-delicate-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-princess-shape-solitaire-studs-earrings-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-50ct-heart-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-oval-shape-halo-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-5ct-emerald-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/round-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-75ct-pear-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-75ct-pear-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-pear-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-5ct-princess-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-solitaire-studs-earrings-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-25ct-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-25ct-round-shape-halo-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-hoops-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-5ct-round-shape-halo-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/3ct-round-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/3ct-emerald-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-25ct-round-shape-halo-studs-earrings-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-dangles-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-25ct-asscher-shape-halo-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-25ct-round-shape-fancy-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/5ct-emerald-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-5ct-round-shape-solitaire-studs-earrings-copy-2/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-halo-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/urban-luxe-diamond-drop-hoops/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/royal-bloom-blue-sapphire-dangler-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-lime-pear-drop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-teardrop-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-two-stone-diamond-drop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-loop-drop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-teardrop-dangle-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/pear-drop-linear-dangler-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-platinum-round-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/celestia-spark-oval-dangles/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/golden-leaf-cascade-diamond-dangle-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-lines-diamond-dangle-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shapem-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-25ct-round-shape-fancy-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-dangles-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-25ct-round-shape-halo-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-50ct-round-shape-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-oval-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/whirlwind-elegance-round-shape-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-solitaire-studs-earrings-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-5ct-round-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-5ct-round-shape-solitaire-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-50-ct-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-5ct-round-shape-dangles-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-solitaire-studs-earrings-2/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-marquise-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-5ct-radiant-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-25ct-round-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-75ct-round-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-5ct-round-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-25ct-emerald-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-fancy-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-5ct-oval-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/3ct-round-shape-solitaire-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-5ct-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/round-shape-fancy-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-5ct-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/0-5ct-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-25ct-round-shape-halo-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1ct-round-shape-fancy-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-75ct-pear-shape-halo-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-emerald-shape-fancy-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-50ct-round-shape-halo-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-54-ctw-round-shape-solitaire-studs-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-75ct-emerald-shape-halo-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2-54-ctw-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-50ct-round-shape-delicate-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/royal-bloom-blue-sapphire-dangler-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-lime-pear-drop-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/regal-radiance-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/2ct-round-shape-delicate-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/diamond-love-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/1-75ct-cushion-shape-halo-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dazzling-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/marquise-sparkle-fancy-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegant-marquise-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/trilogy-blossom-sparkle-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/duet-drop-dazzle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/luminous-marquise-blossom-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sunburst-marquise-sparkle-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/seraphina-halo-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/double-square-halo-drop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/glimmering-floral-burst-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/aurora-drip-teardrop-cluster-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/virelle-spark-marquise-halo-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/regal-fan-cluster-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiance-crest-cushion-halo-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/geometric-bloom-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/luna-gleam-double-halo-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/triarose-spark-halo-shield-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cushion-cut-bezel-set-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/celeste-glow-oval-halo-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegant-emerald-cut-bezel-set-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/stella-spark-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/pear-drop-chevron-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/luminous-duo-sparkle-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/aura-bloom-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-shape-yellow-gold-halo-studs-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/pear-drop-orbit-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/aurelia-bezel-set-round-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/modern-emerald-cascading-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/veloura-halo-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-princess-cut-frame-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cavara-classic-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/serenya-pure-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dazzling-oval-double-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/lunara-essential-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/clover-bloom-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/aeris-true-light-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/caelina-grace-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/isara-eternal-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/geometric-bloom-accent-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/maelis-everyday-luxe-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/evana-classic-light-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-cut-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elowen-classic-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/zarela-everyday-brilliance-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/myla-luxe-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/nerina-glow-lab-diamond-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-cut-halo-stud-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/luminous-marquise-sparkle-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/celestial-spark-diamond-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dazzling-round-brilliant-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/trinity-glow-brilliant-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/effortless-luminosity-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/aurora-bloom-marquise-statement-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/contour-brilliance-marquise-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/orbiting-radiance-drop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/petal-cluster-luminous-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/linear-luxe-teardrop-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/arched-blossom-sparkle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/apex-sparkle-contour-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cosmic-embrace-circle-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/starlight-petal-cluster-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/vertex-sparkle-triangle-frame-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sunburst-tear-pave-bar-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/galactic-swirl-radiance-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/starlight-cascade-pear-drop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sculpted-sparkle-trio-lab-diamond-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/regal-bloom-pave-drop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/aurora-swirl-pave-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/tear-of-light-pave-accent-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/compass-star-halo-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dual-drop-radiance-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/linear-brilliance-cascade-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/the-essential-brilliance-stud-collection-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/the-everyday-sparkle-stud-series-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/round-shape-gorgeous-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dazzling-blossom-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/emerald-shape-gold-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegant-heart-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/asscher-shape-yellow-gold-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/wonderful-round-shape-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-solitaire-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-sparkling-round-shape-solitaire-studs-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-bloom-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/everlume-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/crested-brilliance-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/orbital-sparkle-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/halo-emerald-cut-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/petalglow-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/modern-princess-cut-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sunbeam-floret-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-three-prong-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/enduring-radiance-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dazzling-round-brilliant-stud-earrings-copy-1/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/trinity-luster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/minimalist-trio-prong-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/aurora-petal-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/modern-square-set-round-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/brilliant-round-studs-with-unique-bezel-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-four-prong-solitaire-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/modern-x-prong-solitaire-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegant-emerald-cut-solitaire-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/roseate-lumina-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/whisper-rose-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/timeless-six-prong-round-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/horizon-glow-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-bezel-set-round-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-cluster-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/vista-sparkle-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/everbloom-sparkle-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/double-halo-cushion-cut-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-lumina-cascade-dangles/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/geometric-radiance-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/essential-sparkle-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/triangular-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/celestial-bloom-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/artisan-blossom-diamond-halo-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/aurora-blossom-cluster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/petal-burst-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cascade-silhouette-drops/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cascade-silhouette-drops-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/eternal-circle-hoops/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/luminous-round-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dazzling-floral-cluster-diamond-drop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/celestial-marquise-bloom-diamond-cluster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/curve-diamond-horizon-hoops/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/heartfelt-cascade-diamond-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/orbit-spark-asymmetric-diamond-hoop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-fan-cluster-pear-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/pear-drop-radiance-diamond-halo-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/timeless-brilliance-solitaire-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/diamond-bloom-marquise-and-pear-cluster-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/oval-brilliance-diamond-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dazzling-descent-pear-diamond-drop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/twin-star-dual-diamond-drop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cascading-pear-drop-diamond-statement-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/petal-sparkle-diamond-flower-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cascading-pear-drop-diamond-statement-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/linked-hearts-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiance-multi-cut-diamond-cluster-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/butterfly-heart-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/glamour-pave-diamond-embrace-hoops/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/heart-in-teardrop-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/graceful-line-pear-drop-diamond-hoops/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-square-princess-cut-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegance-diamond-accent-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/entwined-hearts-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/infinity-embrace-pear-halo-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/heart-blossom-diamond-drop-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/allure-emerald-cut-marquise-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/allure-emerald-cut-marquise-diamond-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/infinity-heart-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/blooming-petal-diamond-cluster-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/heartfelt-wings-diamond-cluster-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/artistic-swirl-multi-cut-diamond-cluster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-marquise-burst-diamond-cluster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/loves-radiance-heart-and-trinity-diamond-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/abstract-bloom-intertwined-diamond-cluster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/embracing-heart-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-cascade-marquise-fan-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/hearts-scroll-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/majestic-feathered-cascade-diamond-dangle-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/loves-canopy-heart-and-diamond-drop-studs-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sculpted-petal-solitaire-radiance-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/concentric-radiance-multi-halo-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sparkling-heart-aura-diamond-cluster-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-radiance-pear-drop-diamond-dangle-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/marquise-diamond-hexagon-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-platinum-round-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/luminous-leaf-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cascading-marquise-diamond-hoop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/modern-contours-round-diamond-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/micro-pave-diamond-embrace-hoop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/regal-halo-square-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/convertible-brilliance-round-diamond-hoop-jacket-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/ethereal-blossom-mixed-cut-diamond-cluster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/pave-square-cluster-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-radiance-dual-halo-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/celestial-bloom-radiating-marquise-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/pillow-of-light-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/architectural-brilliance-emerald-cut-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegant-petalette-round-marquise-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/vintage-inspired-milgrain-halo-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sleek-linear-sparkle-diamond-bar-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/art-deco-allure-asscher-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-petal-burst-mixed-cut-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-brilliance-beaded-prong-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/regal-emerald-halo-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/trilogy-sparkle-diamond-cluster-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/modern-edge-bezel-princess-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/timeless-elegance-pear-solitaire-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/streamlined-elegance-bezel-emerald-cut-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/effulgent-cluster-round-brilliant-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/pyramid-of-light-diamond-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/magnificent-double-halo-pear-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/stellar-bloom-diamond-cluster-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegant-oval-halo-brilliance-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/modern-contoured-pear-bezel-set-diamond-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/cosmic-bloom-diamond-cluster-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegance-petals-marquise-round-diamond-cluster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/celestial-triple-gemstone-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/glimmering-cascade-diamond-dangler-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/twinkling-star-cluster-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/radiant-embrace-diamond-micro-pave-hoops-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/channel-set-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/classic-solitaire-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/architectural-gleam-baguette-diamond-hoops-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/princess-cut-solitaire-studs/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/streamlined-shimmer-diamond-bar-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/artful-bloom-mixed-cut-diamond-hoop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/parallel-sparkle-diamond-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/dazzling-drop-halo-stud-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/mosaic-allure-diamond-hoops-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/triple-row-radiance-diamond-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/geometric-gleam-baguette-hoop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/mixed-cut-eternity-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/eternal-twist-diamond-hoop-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/multi-row-pave-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/beaded-frame-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/regal-ascend-emerald-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegant-pave-channel-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/trinity-glow-diamond-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sleek-pave-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/triple-row-pave-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/bezel-set-eternity-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/floral-mirage-diamond-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/double-row-pave-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/multi-row-princess-cut-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/lustre-bloom-cluster-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/marquise-eternity-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/eternal-aura-oval-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/scattered-sparkle-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/wide-channel-set-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/emerald-majesty-double-halo-stud-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/slender-pave-hoop-earrings/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/elegant-dazzle-crystal-dangles-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/sparkling-delta-diamond-dangle-earrings-copy/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/prominent-gemstone-pave-hoops/from_collection=lab-grown-diamonds-earrings",
    "https://geer.in/products/petal-bloom-diamond-cluster-earrings-copy/from_collection=lab-grown-diamonds-earrings"
]


CSV_FILE = "gold_data5.csv"

def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    # Updated fieldnames
    fieldnames = ["Category", "Product URL", "14K Gold Weight", "18K Gold Weight", "Diamond Weight", "Image Link"]
    
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def scrape_geer_product(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_data = {
            "Product URL": url,
            "Category": "N/A",
            "14K Gold Weight": "N/A",
            "18K Gold Weight": "N/A",
            "Diamond Weight": "N/A",
            "Image Link": "N/A"
        }
        
        # 0. Extract Category
        script_tags = soup.find_all("script")
        for script in script_tags:
            if script.string and '"type":' in script.string:
                cat_match = re.search(r'"type"\s*:\s*"([^"]+)"', script.string)
                if cat_match:
                    product_data["Category"] = cat_match.group(1)
                    break
        
        if product_data["Category"] == "N/A":
             breadcrumbs = soup.select(".breadcrumbs a, .breadcrumb a")
             if breadcrumbs:
                 if len(breadcrumbs) >= 2:
                      product_data["Category"] = breadcrumbs[-1].get_text(strip=True)
        
        # 1. Extract Image Link
        og_image = soup.find("meta", property="og:image")
        if og_image:
             product_data["Image Link"] = og_image["content"]
        else:
            img_tag = soup.select_one('.product__media-item img')
            if img_tag:
                 src = img_tag.get('src') or img_tag.get('data-src')
                 if src:
                     if src.startswith('//'):
                         src = 'https:' + src
                     product_data["Image Link"] = src

        # 2. Extract Weights (14K & 18K)
        # Step A: Get Variant Map (ID -> Name) from `var meta`
        variant_map = {}
        
        # Look for: var meta = {"product":{"id":...,"variants":[...]}};
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string and "var meta =" in script.string:
                match = re.search(r'var meta\s*=\s*({.*?});', script.string, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    try:
                        data = json.loads(json_str)
                        if "product" in data and "variants" in data["product"]:
                            for variant in data["product"]["variants"]:
                                v_id = str(variant["id"])
                                # Use public_title if available, else name
                                v_name = variant.get("public_title") or variant.get("name") or ""
                                variant_map[v_id] = v_name
                        break # Found it
                    except json.JSONDecodeError:
                        print("Error parsing var meta JSON")

        # Fallback: JSON-LD Extraction if var meta fails
        if not variant_map:
             json_ld_scripts = soup.find_all('script', type='application/ld+json')
             for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    # Handle list of JSON-LD objects
                    if isinstance(data, list):
                        items = data
                    else:
                        items = [data]
                    
                    for item in items:
                        if item.get('@type') == 'Product' and 'offers' in item:
                            offers = item['offers']
                            if isinstance(offers, dict):
                                offers = [offers]
                            for offer in offers:
                                # offer['url'] usually contains ?variant=ID
                                variant_url = offer.get('url', '')
                                match = re.search(r'variant=(\d+)', variant_url)
                                if match:
                                    variant_id = match.group(1)
                                    variant_name = offer.get('name', '') or item.get('name', '')
                                    if variant_id not in variant_map:
                                         variant_map[variant_id] = variant_name
                except json.JSONDecodeError:
                    continue

        # Step B: Get Price Breakup (ID -> Weight)
        price_breakup_script = soup.find("script", id="variant-price-breakup")
        # Step B: Get Price Breakup (ID -> Weight)
        price_breakup_script = soup.find("script", id="variant-price-breakup")
        if price_breakup_script:
            try:
                price_data = json.loads(price_breakup_script.string)
                
                for variant_id, details in price_data.items():
                    weight = details.get("gold_weight")
                    diamond_wt = details.get("total_diamond_weight") or details.get("diamond_weight")
                    
                    # Check if this variant is 14K or 18K
                    variant_name = variant_map.get(variant_id, "")
                    
                    if "14K" in variant_name:
                         product_data["14K Gold Weight"] = f"{weight} g"
                    elif "18K" in variant_name:
                         product_data["18K Gold Weight"] = f"{weight} g"
                    
                    # Capture diamond weight (usually same for all, just take one)
                    if product_data["Diamond Weight"] == "N/A" and diamond_wt:
                        product_data["Diamond Weight"] = f"{diamond_wt} ct"
                        
            except json.JSONDecodeError:
                print("Error parsing price breakup JSON")

        # 4. Fallback for Diamond Weight (Regex on Page Text)
        if product_data["Diamond Weight"] == "N/A":
            page_text = soup.get_text()
            
            # Pattern 1: Diamond (2.0ct) - specific to Price Breakup UI
            d_match = re.search(r"Diamond\s*\(\s*(\d+\.?\d*)\s*ct\s*\)", page_text, re.IGNORECASE)
            if d_match:
                product_data["Diamond Weight"] = d_match.group(1) + " ct"
            
            # Pattern 2: "total weight of 2.0 carats" - specific to Description
            if product_data["Diamond Weight"] == "N/A":
                d_match = re.search(r"total\s*weight\s*of\s*(\d+\.?\d*)\s*carats?", page_text, re.IGNORECASE)
                if d_match:
                    product_data["Diamond Weight"] = d_match.group(1) + " ct"
            
            # Pattern 3: Generic "2.0 ct Diamond" or "Diamond Weight: 2.0 ct"
            if product_data["Diamond Weight"] == "N/A":
                 d_match = re.search(r"Diamond.*?Weight.*?(\d+\.?\d*)\s*ct", page_text, re.IGNORECASE)
                 if d_match:
                     product_data["Diamond Weight"] = d_match.group(1) + " ct"

        return product_data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

if __name__ == "__main__":
    print(f"Starting scrape for {len(URLS)} products...")
    
    for url in URLS:
        print(f"Scraping {url}...")
        data = scrape_geer_product(url)
        
        if data:
            print(f"Success! Category: {data.get('Category')}")
            print(f"14K Gold: {data.get('14K Gold Weight')}")
            print(f"18K Gold: {data.get('18K Gold Weight')}")
            save_to_csv(data, CSV_FILE)
        else:
            print(f"Failed to scrape {url}")
        
        print("-" * 30)
    print("Batch scraping completed.")
