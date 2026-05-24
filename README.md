<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 220" width="900" height="220" role="img" aria-label="Currently building: Axylith">
  <defs>
    <linearGradient id="bg-ax" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d0e10"/>
      <stop offset="100%" stop-color="#13151a"/>
    </linearGradient>
    <linearGradient id="acc-ax" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c89858"/>
      <stop offset="100%" stop-color="#b88848"/>
    </linearGradient>
    <pattern id="grid-ax" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1f2126" stroke-width="0.5"/>
    </pattern>
  </defs>

  <rect width="900" height="220" fill="url(#bg-ax)" rx="6"/>
  <rect width="900" height="220" fill="url(#grid-ax)" opacity="0.4"/>

  <!-- Header strip -->
  <text x="30" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#5a5249" letter-spacing="2">
    CURRENTLY BUILDING
  </text>
  <line x1="30" y1="42" x2="870" y2="42" stroke="#2a2d34" stroke-width="1"/>

  <!-- Main content area, two columns -->

  <!-- Left: project name + description -->
  <g font-family="JetBrains Mono, monospace">
    <text x="30" y="84" fill="#e8dcc8" font-size="32" font-weight="500" letter-spacing="-0.5">
      axylith
    </text>
    <text x="195" y="84" fill="url(#acc-ax)" font-size="11" letter-spacing="1.5">
      ● PRE-V1
    </text>

    <text x="30" y="116" fill="#8b8275" font-size="13" letter-spacing="0">
      a native research environment
    </text>

    <text x="30" y="148" fill="#7a7268" font-size="11" letter-spacing="0">
      one binary integrating prose, code, data, and 3D geometry,
    </text>
    <text x="30" y="164" fill="#7a7268" font-size="11" letter-spacing="0">
      with an AI layer that can reason across all of them.
    </text>

    <text x="30" y="196" fill="#c89858" font-size="11" letter-spacing="1">
      github.com/Axylith/axle  →
    </text>
  </g>

  <!-- Right: tech stack -->
  <g font-family="JetBrains Mono, monospace">
    <text x="540" y="84" fill="#5a5249" font-size="10" letter-spacing="1.5">STACK</text>
    <line x1="540" y1="92" x2="870" y2="92" stroke="#2a2d34" stroke-width="0.5"/>

    <text x="540" y="116" fill="#8b8275" font-size="11">
      <tspan fill="#5a5249">language</tspan>
      <tspan x="640" fill="#e8dcc8">C++20</tspan>
    </text>
    <text x="540" y="136" fill="#8b8275" font-size="11">
      <tspan fill="#5a5249">graphics</tspan>
      <tspan x="640" fill="#e8dcc8">Vulkan 1.3</tspan>
    </text>
    <text x="540" y="156" fill="#8b8275" font-size="11">
      <tspan fill="#5a5249">platform</tspan>
      <tspan x="640" fill="#e8dcc8">Linux / X11</tspan>
    </text>
    <text x="540" y="176" fill="#8b8275" font-size="11">
      <tspan fill="#5a5249">format</tspan>
      <tspan x="640" fill="#e8dcc8">custom .axl</tspan>
    </text>
    <text x="540" y="196" fill="#8b8275" font-size="11">
      <tspan fill="#5a5249">license</tspan>
      <tspan x="640" fill="#e8dcc8">AGPL v3</tspan>
    </text>
  </g>
</svg>
