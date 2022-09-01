// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Ponto de Controle',
  tagline: 'A Cartografia Documentada',
  url: 'https://github.com/dsgoficial',
  baseUrl: '/pto_controle/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'dsgoficial', // Usually your GitHub org/user name.
  projectName: 'pto_controle', // Usually your repo name.
  deploymentBranch: 'gh-pages',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Ponto de Controle',
        
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Guia de Aplicação',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentos',
            items: [
              {
                label: 'Guia de Aplicação',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Organizações Militares',
            items: [
              {
                label: 'DSG',
                href: 'http://www.dsg.eb.mil.br/',
              },
              {
                label: '1º CGEO',
                href: 'http://www.1cgeo.eb.mil.br/',
              },
            ],
          },
          {
            title: 'Mais',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/1cgeo',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} DGEO - 1º CGEO. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;