// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Organização de Pontos de Controle',
  tagline: '',
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
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },

  plugins:[
    [require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: "en"
      }
    ]
  ],

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
          {
            type: 'doc',
            docId: 'manual_medidor',
            position: 'left',
            label: 'Manual do Medidor',
          },
          {
            type: 'doc',
            docId: 'exemplos',
            position: 'left',
            label: 'Exemplos',
          },
          {
            type: 'doc',
            docId: 'erros_comuns/npm_proxy',
            position: 'left',
            label: 'Erros Comuns',
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
              {
                label: 'PPP-IBGE',
                href: 'https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=o-que-e'
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
            ],
          },
          {
            title: 'Mais',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/dsgoficial',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Diretoria de Serviço Geográfico. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;