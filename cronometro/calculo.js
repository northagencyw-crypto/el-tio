/* EL TIO - el calculo del Cronometro.

   Funcion pura, sin DOM, para poder probarla en Node (pruebas/cronometro.test.js)
   y usarla igual en el navegador. Todas las cifras salen de lo que escribe el
   dueno. El unico numero que no es suyo es el supuesto de cuantos clientes se
   van por la demora, y viene con un valor de partida que el dueno cambia.

   Formulas:
     esperanPorDia = mensajes * (1 - fueraDeHorario) * esperaEnHorario
                   + mensajes * fueraDeHorario * esperaDeNoche
     esperanAlMes  = esperanPorDia * diasAlMes
     ventasEnJuego = esperanAlMes * (compranDeCada10 / 10)
     dineroEnJuego = ventasEnJuego * ticket
     perdidaEstimada = dineroEnJuego * (seVanDeCada10 / 10)

   esperaEnHorario y esperaDeNoche valen 1 si la respuesta del dueno es de mas
   de una hora (mas de una hora, a la manana siguiente o a veces no contesto)
   y 0 si contesta dentro de la hora. */
(function (raiz) {
  'use strict';

  var ESPERA_MAS_DE_UNA_HORA = {
    rapido: 0,   // menos de 15 minutos
    hora: 0,     // dentro de la hora
    mas: 1,      // mas de una hora
    manana: 1,   // a la manana siguiente
    nunca: 1     // a veces no contesto
  };

  function numero(v, min, max, porDefecto) {
    var n = typeof v === 'number' ? v : parseFloat(String(v == null ? '' : v).replace(',', '.'));
    if (!isFinite(n)) return porDefecto;
    return Math.min(max, Math.max(min, n));
  }

  function calcular(e) {
    e = e || {};
    var mensajes = numero(e.mensajes, 0, 5000, 0);
    var fuera = numero(e.fueraDeHorario, 0, 1, 0);
    var esperaDia = ESPERA_MAS_DE_UNA_HORA[e.respuestaHorario] || 0;
    var esperaNoche = ESPERA_MAS_DE_UNA_HORA[e.respuestaNoche] || 0;
    var compran = numero(e.compranDeCada10, 0, 10, 0);
    var dias = numero(e.diasAlMes, 1, 31, 30);
    var seVan = numero(e.seVanDeCada10, 0, 10, 2);
    var hayTicket = e.ticket !== '' && e.ticket != null && isFinite(parseFloat(String(e.ticket).replace(',', '.')));
    var ticket = hayTicket ? numero(e.ticket, 0, 10000000, 0) : null;

    var enHorario = mensajes * (1 - fuera) * esperaDia;
    var deNoche = mensajes * fuera * esperaNoche;
    var esperanPorDia = enHorario + deNoche;
    var esperanAlMes = esperanPorDia * dias;
    var ventasEnJuego = esperanAlMes * (compran / 10);
    var dineroEnJuego = ticket === null ? null : ventasEnJuego * ticket;
    var perdidaEstimada = dineroEnJuego === null ? null : dineroEnJuego * (seVan / 10);

    return {
      entradas: {
        mensajes: mensajes, fueraDeHorario: fuera, esperaEnHorario: esperaDia,
        esperaDeNoche: esperaNoche, compranDeCada10: compran, diasAlMes: dias,
        seVanDeCada10: seVan, ticket: ticket
      },
      esperanEnHorarioPorDia: enHorario,
      esperanDeNochePorDia: deNoche,
      esperanPorDia: esperanPorDia,
      esperanAlMes: Math.round(esperanAlMes),
      ventasEnJuego: Math.round(ventasEnJuego),
      dineroEnJuego: dineroEnJuego === null ? null : Math.round(dineroEnJuego),
      perdidaEstimada: perdidaEstimada === null ? null : Math.round(perdidaEstimada),
      // Donde esta el problema, para elegir el consejo.
      foco: esperanPorDia === 0 ? 'ninguno' : (deNoche >= enHorario ? 'noche' : 'horario')
    };
  }

  var api = { calcular: calcular, ESPERA_MAS_DE_UNA_HORA: ESPERA_MAS_DE_UNA_HORA };
  if (typeof module === 'object' && module.exports) module.exports = api;
  else raiz.CronometroCalculo = api;
})(this);
