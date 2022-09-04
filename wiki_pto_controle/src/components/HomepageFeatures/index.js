import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';

const FeatureList = [
  {
    title: 'Guia de Aplicação',
    link: 'docs/category/guia-de-uso',
    description: (
      <>
        Realize a padronização dos Pontos de Controle coletados, gere monografias automáticas e gerencie informações dentro de um Banco de Dados.
      </>
    ),
  },
  {
    title: 'Erros Comuns',
    link: 'docs/category/problemas-comuns',
    description: (
      <>
        Encontre a solução para os erros mais comuns, realize colaborações e aponte melhorias.
      </>
    ),
  },
  {
    title: 'Exemplos',
    link: 'docs/exemplos',
    description: (
      <>
        Acesso a uma pasta modelo, que contém os arquivos a serem processados no Guia de Aplicação.
      </>
    ),
  },
];

function Feature({Svg, title, description, link}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3><Link to={link}>{title}</Link></h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
