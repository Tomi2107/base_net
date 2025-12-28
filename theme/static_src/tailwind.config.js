const colors = require('tailwindcss/colors')

module.exports = {
    mode: "jit",

    purge: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        '../../**/templates/**/**/*.html',
    ],

    darkMode: 'class', // ✅ FIX CLAVE

    theme: {
        extend: {
            colors: {
                'dark-main': '#18191A',
                'dark-second': '#242526',
                'dark-third': '#3A3B3C',
                'dark-txt': '#B8BBBF',
                sky: colors.sky,
                teal: colors.teal,
                rose: colors.rose,
            },
        },
    },

    safelist: ['dark'],

    variants: {
        extend: {
            display: ['group-hover'],
            transform: ['group-hover'],
            scale: ['group-hover'],
            textOpacity: ['dark'],
        },
    },

    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
        require('tailwind-scrollbar-hide'),
    ],
}
