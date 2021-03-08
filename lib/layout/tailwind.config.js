const plugin = require('tailwindcss/plugin')

module.exports = {
  purge: [],
  prefix: '',
  important: false,
  separator: ':',
  theme: {
    extend: {
      backgroundImage: theme => ({
        'topographic': "url('../svg/hero-topo.svg')",
      }),
      fill: theme => ({
        'topo-green': theme('colors.green') + '4a',
      }),
      lineHeight: {
        "cuddly": "0.8rem"
      },
    },
    screens: {
      'sm': {'max': '768px'},
      'md': {'min': '768px'},
      'lg': {'min': '1024px'},
      'xl': {'min': '1280px'},
    },
    colors: {
      transparent: 'transparent',
      current: 'currentColor',

      black: '#263138',
      white: '#fff',

      gray: {
        100: '#fcfdfd',
        200: '#e5eaed',
        300: '#ced7dd',
        400: '#b7c4cd',
        500: '#9fb1be',
        600: '#889fae',
        700: '#718c9e',
        800: '#465966',
        900: '#36454f'
      },
      glass: {
        100: '#fcfdfd60',
        200: '#e5eaed60',
        300: '#ced7dd60',
        400: '#b7c4cd60',
        500: '#9fb1be60',
        600: '#889fae60',
        700: '#718c9e60',
        800: '#46596660',
        900: '#36454f60'
      },
      blue: '#2d4066',
      indigo: '#595e8d',
      purple: '#6e598d',
      pink: '#a67391',
      red: '#9f2d45',
      orange: '#d1733a',
      yellow: '#b8965b',
      green: '#73a688',
      teal: '#2d5c66',
      cyan: '#02b3c3'
    },
    spacing: {
      px: '1px',
      '0': '0',
      '1': '0.25rem',
      '2': '0.5rem',
      '3': '0.75rem',
      '4': '1rem',
      '5': '1.25rem',
      '6': '1.5rem',
      '8': '2rem',
      '10': '2.5rem',
      '12': '3rem',
      '16': '4rem',
      '20': '5rem',
      '24': '6rem',
      '32': '8rem',
      '40': '10rem',
      '48': '12rem',
      '56': '14rem',
      '64': '16rem',
      '96': '24rem',
      '128': '32rem',
      'vw': '100vw',
      'vh': '100vh'
    },
    borderColor: theme => ({
      ...theme('colors'),
      default: theme('colors.gray.300', 'currentColor'),
    }),
    boxShadow: {
      xs: '0 0 0 1px rgba(0, 0, 0, 0.05)',
      sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      default: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
      inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
      outline: '0 0 0 3px rgba(66, 153, 225, 0.5)',
      none: 'none',
      'btn-teal': '5px 5px 5px 0 rgba(45, 92, 102, 0.5)'
    },
    fontFamily: {
      sans: ['Lato', 'sans-serif'],
      serif: ['Crimson Text', 'serif'],
      mono: ['Inconsolata', 'monospace'],
    },
    fontSize: { // http://www.layoutgridcalculator.com/typographic-scale/
      xs: '0.75rem',
      sm: '0.8333rem',
      base: '0.9167rem',
      lg: '1rem',
      xl: '1.1042rem',
      '2xl': '1.4792rem',
      '3xl': '1.7917rem',
      '4xl': '2.8958rem',
      '5xl': '3.8542rem',
      '6xl': '3.8542rem',
      'title': '3.8542rem',
    },
    height: theme => ({
      auto: 'auto',
      ...theme('spacing'),
      full: '100%',
      screen: '100vh',
      thumbnail: '200px'
    }),
    margin: (theme, { negative }) => ({
      auto: 'auto',
      "nudge": "10%",
      ...theme('spacing'),
      ...negative(theme('spacing')),
    }),
    maxHeight: {
      full: '100%',
      screen: '100vh',
      thumbnail: '200px',
    },
    maxWidth: (theme, { breakpoints }) => ({
      none: 'none',
      xs: '20rem',
      sm: '24rem',
      md: '28rem',
      lg: '32rem',
      xl: '36rem',
      '2xl': '42rem',
      '3xl': '48rem',
      '4xl': '56rem',
      '5xl': '64rem',
      '6xl': '72rem',
      full: '100%',
      thumbnail: '200px',
      fit: 'fit-content',
      max: 'max-content',
      min: 'min-content',
      ...breakpoints(theme('screens')),
    }),
    minHeight: (theme) => ({
      '0': '0',
      full: '100%',
      screen: '100vh',
      ...theme('spacing'),
    }),
    width: theme => ({
      auto: 'auto',
      ...theme('spacing'),
      '1/2': '50%',
      '1/3': '33.333333%',
      '2/3': '66.666667%',
      '1/4': '25%',
      '2/4': '50%',
      '3/4': '75%',
      '1/5': '20%',
      '2/5': '40%',
      '3/5': '60%',
      '4/5': '80%',
      '1/6': '16.666667%',
      '2/6': '33.333333%',
      '3/6': '50%',
      '4/6': '66.666667%',
      '5/6': '83.333333%',
      '1/12': '8.333333%',
      '2/12': '16.666667%',
      '3/12': '25%',
      '4/12': '33.333333%',
      '5/12': '41.666667%',
      '6/12': '50%',
      '7/12': '58.333333%',
      '8/12': '66.666667%',
      '9/12': '75%',
      '10/12': '83.333333%',
      '11/12': '91.666667%',
      full: '100%',
      screen: '100vw',
      thumbnail: '200px',
      double: '200%',
      triple: '300%',
    }),
    zIndex: {
      auto: 'auto',
      '0': '0',
      '10': '10',
      '20': '20',
      '30': '30',
      '40': '40',
      '50': '50',
    },
    // https://github.com/benface/tailwindcss-gradients#advanced
    linearGradientColors: theme => ({
      'teal-cyan': [theme('colors.teal'), theme('colors.cyan')],
      'active-button': [
        theme('colors.blue'),
        theme('colors.teal') + " 30%",
        theme('colors.teal') + " 70%",
        theme('colors.blue')
      ]
    }),
    filter: { // defaults to {}
      'none': 'none',
      'grayscale': 'grayscale(1)',
      'invert': 'invert(1)',
      'sepia': 'sepia(1)',
    },
    backdropFilter: { // defaults to {}
      'none': 'none',
      'blur': 'blur(2px)',
    },
  },
  variants: {
    extend: {
      backgroundColor: ['active', 'focus-within', 'group-focus', 'parent-hover'],
      backgroundOpacity: ['active'],
      borderColor: ['active', 'group-focus', 'parent-hover'],
      borderOpacity: ['active'],
      borderRadius: ['first', 'last'],
      borderStyle: ['first', 'last'],
      borderWidth: ['first', 'last', 'active'],
      boxShadow: ['first', 'last', 'active'],
      cursor: ['active'],
      display: ['group-hover', 'group-focus', 'parent-hover'],
      linearGradients: ['first', 'last', 'active'],
      margin: ['first', 'last'],
      padding: ['first', 'last'],
      ringWidth: ['active'],
      ringColor: ['active', 'group-focus', 'parent-hover'],
    },
    filter: ['responsive', 'hover', 'focus'], // defaults to ['responsive']
    backdropFilter: ['responsive', 'hover', 'focus'], // defaults to ['responsive']
  },
  corePlugins: {},
  plugins: [
    require('@tailwindcss/forms'),
    require('tailwindcss-gradients'),
    require('tailwindcss-filters'),
    plugin(function({ addUtilities }) {
      const newUtilities = {
        '.slight-tilt': {
          transform: 'perspective(9000000px) rotateX(15deg)',
        }
      }

      addUtilities(newUtilities)
    }),
    // Expand the `active` variant to also select for the presence of a boolean attribute or a class.
    plugin(function({ addVariant, e }) {
      addVariant('active', ({ modifySelectors, separator }) => {
        modifySelectors(({ className }) => {
          return `
            .${e(`active${separator}${className}`)}[active], 
            .${e(`active${separator}${className}`)}:active, 
            .${e(`active${separator}${className}`)}.active
          `
        })
      })
    }),
    // Add a `parent-hover` variant to complement `group-hover`.
    plugin(function({ addVariant, e }) {
      addVariant('parent-hover', ({ modifySelectors, separator }) => {
        modifySelectors(({ className }) => {
          return `.hovering-parent:hover > .${
            e(`parent-hover${separator}${className}`)}`
        })
      })
    })
  ],
}
