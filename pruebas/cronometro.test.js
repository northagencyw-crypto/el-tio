// Pruebas del calculo del Cronometro. Correr con: node --test pruebas/cronometro.test.js
// Los resultados esperados estan hechos a mano, linea por linea.
const test = require('node:test');
const assert = require('node:assert/strict');
const { calcular } = require('../cronometro/calculo.js');

test('caso 1: restaurante que contesta rapido de dia y a la manana siguiente de noche', () => {
  // 20 por dia, 1 de cada 4 fuera de horario -> 5 esperan por dia.
  // 5 * 30 = 150 al mes. 150 * 3/10 = 45 ventas. 45 * 500 = 22 500.
  // 22 500 * 2/10 = 4 500.
  const r = calcular({
    mensajes: 20, fueraDeHorario: 0.25, respuestaHorario: 'rapido', respuestaNoche: 'manana',
    compranDeCada10: 3, ticket: 500, diasAlMes: 30, seVanDeCada10: 2
  });
  assert.equal(r.esperanPorDia, 5);
  assert.equal(r.esperanAlMes, 150);
  assert.equal(r.ventasEnJuego, 45);
  assert.equal(r.dineroEnJuego, 22500);
  assert.equal(r.perdidaEstimada, 4500);
  assert.equal(r.foco, 'noche');
});

test('caso 2: tarda mas de una hora de dia y a veces no contesta de noche', () => {
  // 40 por dia: 20 en horario + 20 de noche, todos esperan -> 40 por dia.
  // 40 * 26 = 1 040. 1 040 * 2/10 = 208 ventas. 208 * 1 200 = 249 600.
  // 249 600 * 3/10 = 74 880.
  const r = calcular({
    mensajes: 40, fueraDeHorario: 0.5, respuestaHorario: 'mas', respuestaNoche: 'nunca',
    compranDeCada10: 2, ticket: '1200', diasAlMes: 26, seVanDeCada10: 3
  });
  assert.equal(r.esperanPorDia, 40);
  assert.equal(r.esperanAlMes, 1040);
  assert.equal(r.ventasEnJuego, 208);
  assert.equal(r.dineroEnJuego, 249600);
  assert.equal(r.perdidaEstimada, 74880);
});

test('caso 3: contesta dentro de la hora y no pone ticket', () => {
  const r = calcular({
    mensajes: 10, fueraDeHorario: 0.1, respuestaHorario: 'hora', respuestaNoche: 'rapido',
    compranDeCada10: 5, ticket: '', diasAlMes: 30, seVanDeCada10: 2
  });
  assert.equal(r.esperanAlMes, 0);
  assert.equal(r.ventasEnJuego, 0);
  assert.equal(r.dineroEnJuego, null);
  assert.equal(r.perdidaEstimada, null);
  assert.equal(r.foco, 'ninguno');
});

test('entradas fuera de rango se acotan', () => {
  const r = calcular({
    mensajes: -5, fueraDeHorario: 3, respuestaHorario: 'x', respuestaNoche: 'manana',
    compranDeCada10: 40, ticket: 'abc', diasAlMes: 99, seVanDeCada10: -1
  });
  assert.equal(r.entradas.mensajes, 0);
  assert.equal(r.entradas.fueraDeHorario, 1);
  assert.equal(r.entradas.compranDeCada10, 10);
  assert.equal(r.entradas.diasAlMes, 31);
  assert.equal(r.entradas.seVanDeCada10, 0);
  assert.equal(r.dineroEnJuego, null);
});
