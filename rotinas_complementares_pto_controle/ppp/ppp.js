/**
 ***************************************************************************
 * Name            : Processamento PPP em lote
 * Description     : Realiza o download do ponto processado por PPP do IBGE em lote baseado nos arquivos RINEX de medição
 * Version         : 1.0
 * copyright       : 1ºCGEO / DSG
 * reference
 ***************************************************************************
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************
 */

import { Selector } from "testcafe";

import { lstatSync, readdirSync } from "fs";
const path = require('path')

const findPPP = dir => {
  let zips = [];
  readdirSync(dir).forEach(file => {
    const filepath = path.join(dir, file);
    if (lstatSync(filepath).isDirectory()) {
      zips = [...zips, ...findPPP(filepath)];
    } else if (
      lstatSync(filepath).isFile() &&
      filepath.split(".")[filepath.split(".").length - 1] == "zip" &&
      filepath.split(path.sep)[filepath.split(path.sep).length - 2] == "2_RINEX"
    ) {
      zips.push(filepath);
    }
  });
  return zips;
};

const removeDownloaded = dir => {
  let zips = [];
  readdirSync(dir).forEach(file => {
    const pto_regex = /^([A-Z]{2})-(HV|Base|BASE)-[1-9]+[0-9]*$/;
    if (
      lstatSync(path.join(dir, file)).isFile() &&
      file.split(".")[file.split(".").length - 1] == "zip" &&
      file.split("_").length == 4 &&
      pto_regex.test(file.split("_")[1].slice(0, -4))
    ) {
      zips.push(file.split("_")[1].slice(0, -4));
    }
  });
  return pto_path => {
    let pto = pto_path
      .split(path.sep)
      [pto_path.split(path.sep).length - 1].slice(0, -4);
    if (zips.indexOf(pto) > -1) {
      return false;
    } else {
      return true;
    }
  };
};


let zips = findPPP(process.argv[6]);

zips = zips.filter(removeDownloaded(process.argv[7]));

fixture `Test`
    .page `https://www.ibge.gov.br/geociencias-novoportal/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados`

zips.forEach(zip => {
  let name =
  "Download: " + zip.split("\\")[zip.split("\\").length - 1].slice(0, -4);
  
  test(name, async t => {
      await t
        // .click(Selector("a").withText("Processar os dados"))
        .typeText(
          Selector("input").withAttribute("name", "email"),
          process.argv[8]
        )
        .setFilesToUpload(
          Selector("input").withAttribute("name", "arquivo"),
          zip
        )
        .click(Selector("input").withAttribute("value", "Processar"))
        .wait(30000)
        .switchToIframe("#iframe_resultado")
        .wait(30000)
        .click(Selector("body > div > button"))
        .wait(30000);
  });
});