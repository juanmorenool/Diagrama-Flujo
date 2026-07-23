import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="T_Credito — Pipeline revolver de tarjetas", layout="centered")

# ---------------------------------------------------------------------------
# Estilos (se inyectan una sola vez y aplican a todo lo que renderizamos con
# st.markdown(..., unsafe_allow_html=True) más abajo, que SÍ vive en la página
# principal y por lo tanto hace scroll normal junto con el resto de la app).
# ---------------------------------------------------------------------------
st.markdown("""
<style>
  .block-container { max-width: 760px; padding-top: 2rem; }
  h1.pt { font-size: 22px; font-weight: 700; color: #2C2C2A; margin: 0 0 4px; }
  p.sub { font-size: 13px; font-style: italic; color: #5F5E5A; margin: 0 0 20px; }
  h2.sec { font-size: 16px; font-weight: 700; color: #2C2C2A; margin: 0 0 10px; }
  h3.subsec { font-size: 14.5px; font-weight: 700; color: #2C2C2A; margin: 18px 0 6px; }
  section.blk { border-top: 1px solid #D8D6CC; padding-top: 20px; margin-top: 28px; }
  p.body { font-size: 14.5px; line-height: 1.65; color: #33322E; margin: 0 0 14px; }
  code.field { font-family: "SF Mono", Consolas, monospace; font-size: 13px; background: #F1EFE8;
               color: #2C2C2A; padding: 1px 5px; border-radius: 4px; }
  table.io { width: 100%; border-collapse: collapse; margin: 8px 0 4px; font-size: 13.5px; }
  table.io th { text-align: left; font-weight: 700; color: #2C2C2A; border-bottom: 1px solid #D8D6CC; padding: 6px 8px; }
  table.io td { padding: 6px 8px; border-bottom: 1px solid #EDEBE3; color: #33322E; vertical-align: top; }
  .notes-tag { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.04em;
               text-transform: uppercase; color: #854F0B; background: #FAEEDA; padding: 2px 8px;
               border-radius: 4px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="pt">Pipeline T_Credito — documentación funcional</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub">Interbank Perú. Lógica del código, inputs y outputs reales del modelo. Notas metodológicas al final.</p>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DIAGRAMA — único bloque que va en un iframe (components.html). Altura fija
# porque el SVG tiene un tamaño conocido; no necesita crecer ni scrollear.
# ---------------------------------------------------------------------------
SVG_DIAGRAM = """
<div style="background:#FFFFFF;border:1px solid #DAD8CE;border-radius:12px;padding:24px;
            font-family:-apple-system,'Segoe UI',Arial,sans-serif;">
<svg width="100%" viewBox="0 0 680 540" role="img" xmlns="http://www.w3.org/2000/svg">
<title>Pipeline de modelado revolver tarjetas de crédito Interbank</title>
<desc>Diagrama de flujo: inputs transaccionales y macro, segmentación conductual, modelos de utilización y amortización, y outputs finales.</desc>
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="#5F5E5A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
<style>
  .t  { font: 400 14px/1.3 -apple-system, 'Segoe UI', Arial, sans-serif; }
  .ts { font: 400 12px/1.3 -apple-system, 'Segoe UI', Arial, sans-serif; }
  .th { font: 600 14px/1.3 -apple-system, 'Segoe UI', Arial, sans-serif; }
</style>

<rect x="60" y="40" width="260" height="56" rx="8" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5"/>
<text class="th" x="190" y="58" text-anchor="middle" dominant-baseline="central" fill="#2C2C2A">Datos transaccionales</text>
<text class="ts" x="190" y="76" text-anchor="middle" dominant-baseline="central" fill="#444441">Cliente, saldo, pago</text>

<rect x="340" y="40" width="260" height="56" rx="8" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5"/>
<text class="th" x="470" y="58" text-anchor="middle" dominant-baseline="central" fill="#2C2C2A">Datos macroeconómicos</text>
<text class="ts" x="470" y="76" text-anchor="middle" dominant-baseline="central" fill="#444441">ICC, desempleo, spread</text>

<line x1="190" y1="96" x2="250" y2="140" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>
<line x1="470" y1="96" x2="430" y2="140" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="190" y="140" width="300" height="64" rx="8" fill="#FAEEDA" stroke="#854F0B" stroke-width="0.5"/>
<text class="th" x="340" y="162" text-anchor="middle" dominant-baseline="central" fill="#412402">Segmentación conductual</text>
<text class="ts" x="340" y="182" text-anchor="middle" dominant-baseline="central" fill="#633806">Ventana 6m, umbral 95%</text>

<path d="M340 204 L340 232 L190 232 L190 260" fill="none" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>
<path d="M340 204 L340 232 L430 232 L430 260" fill="none" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="100" y="260" width="180" height="56" rx="8" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5"/>
<text class="th" x="190" y="280" text-anchor="middle" dominant-baseline="central" fill="#2C2C2A">Totalero</text>
<text class="ts" x="190" y="298" text-anchor="middle" dominant-baseline="central" fill="#444441">Excluido de IRRBB</text>

<rect x="340" y="260" width="180" height="56" rx="8" fill="#FAEEDA" stroke="#854F0B" stroke-width="0.5"/>
<text class="th" x="430" y="280" text-anchor="middle" dominant-baseline="central" fill="#412402">Revolver</text>
<text class="ts" x="430" y="298" text-anchor="middle" dominant-baseline="central" fill="#633806">Continúa pipeline</text>

<path d="M430 316 L430 328 L190 328 L190 340" fill="none" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>
<path d="M430 316 L430 328 L490 328 L490 340" fill="none" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="60" y="340" width="260" height="64" rx="8" fill="#E6F1FB" stroke="#185FA5" stroke-width="0.5"/>
<text class="th" x="190" y="362" text-anchor="middle" dominant-baseline="central" fill="#042C53">Utilización (SARIMAX)</text>
<text class="ts" x="190" y="382" text-anchor="middle" dominant-baseline="central" fill="#0C447C">Saldo/Límite + exógenas</text>

<rect x="360" y="340" width="260" height="64" rx="8" fill="#E6F1FB" stroke="#185FA5" stroke-width="0.5"/>
<text class="th" x="490" y="362" text-anchor="middle" dominant-baseline="central" fill="#042C53">Amortización (Logit+OLS)</text>
<text class="ts" x="490" y="382" text-anchor="middle" dominant-baseline="central" fill="#0C447C">Spread + desempleo lag2</text>

<line x1="190" y1="404" x2="190" y2="440" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>
<line x1="490" y1="404" x2="490" y2="440" stroke="#5F5E5A" stroke-width="1" marker-end="url(#arrow)"/>

<rect x="60" y="440" width="260" height="56" rx="8" fill="#EAF3DE" stroke="#3B6D11" stroke-width="0.5"/>
<text class="th" x="190" y="460" text-anchor="middle" dominant-baseline="central" fill="#173404">Tasa_Utilizacion</text>
<text class="ts" x="190" y="478" text-anchor="middle" dominant-baseline="central" fill="#27500A">Utilizacion_Fitted</text>

<rect x="360" y="440" width="260" height="56" rx="8" fill="#EAF3DE" stroke="#3B6D11" stroke-width="0.5"/>
<text class="th" x="490" y="460" text-anchor="middle" dominant-baseline="central" fill="#173404">Tasa_Pago_Mensual</text>
<text class="ts" x="490" y="478" text-anchor="middle" dominant-baseline="central" fill="#27500A">TPR_Predicho</text>

<rect x="60" y="513" width="12" height="12" rx="2" fill="#B4B2A9"/>
<text class="ts" x="78" y="522" fill="#444441">Input</text>
<rect x="160" y="513" width="12" height="12" rx="2" fill="#EF9F27"/>
<text class="ts" x="178" y="522" fill="#444441">Segmentación</text>
<rect x="300" y="513" width="12" height="12" rx="2" fill="#378ADD"/>
<text class="ts" x="318" y="522" fill="#444441">Procesamiento</text>
<rect x="460" y="513" width="12" height="12" rx="2" fill="#639922"/>
<text class="ts" x="478" y="522" fill="#444441">Output</text>
</svg>
</div>
"""

# height debe cubrir el card completo (svg 540 + padding 48). Si algún día
# agrandas el diagrama, sube este número acorde al viewBox height + ~50.
components.html(SVG_DIAGRAM, height=600, scrolling=False)

# ---------------------------------------------------------------------------
# TEXTO — todo esto va con st.markdown (NO components.html), así que vive en
# la página normal de Streamlit y hace scroll junto con el resto de la app.
# ---------------------------------------------------------------------------
st.markdown("""
<p class="body" style="margin-top:28px;">El pipeline recibe dos tablas de entrada y produce, en tres etapas
secuenciales, la clasificación conductual de la cartera y las dos series que alimentan la proyección de
flujos para IRRBB. A continuación se detalla la lógica de cada etapa del código y los campos reales que
entran y salen del modelo.</p>

<section class="blk">
  <h2 class="sec">Inputs reales</h2>
  <table class="io">
    <tr><th>Tabla</th><th>Campos</th></tr>
    <tr><td><code class="field">df_transaccional</code></td><td>ID_Cliente, Fecha, Limite_Credito, Saldo_Facturado, Monto_Pagado</td></tr>
    <tr><td><code class="field">df_macro</code></td><td>ICC_Puntos, Masa_Salarial_Indice, Estacionalidad_Julio, Estacionalidad_Diciembre, Tasa_Desempleo_Pct, Spread_TC_PP</td></tr>
  </table>
</section>

<section class="blk">
  <h2 class="sec">Etapa 1 — Segmentación conductual</h2>
  <p class="body">El código ordena <code class="field">df_transaccional</code> por cliente y fecha, y fija dos
  parámetros: <code class="field">VENTANA_MESES = 6</code> y <code class="field">UMBRAL_TOLERANCIA = 0.95</code>.
  Para cada registro calcula <code class="field">Ratio_Pago = Monto_Pagado / Saldo_Facturado</code> (asignando
  1.0 cuando el saldo es cero) y la bandera <code class="field">Es_Mes_Pagador</code>, que toma valor 1 si el
  ratio es al menos 0.95.</p>
  <p class="body">Sobre esa bandera aplica un mínimo móvil de 6 meses por cliente. Si el mínimo de la ventana es
  1, el cliente pagó la totalidad en todos los meses observados y se clasifica como <strong>Totalero</strong>.
  Si el mínimo cae a 0 en algún punto, se clasifica como <strong>Revolver</strong>. El resultado queda en la
  columna <code class="field">Segmento_Conductual</code>, y solo el segmento Revolver continúa a las etapas
  siguientes.</p>
</section>

<section class="blk">
  <h2 class="sec">Etapa 2 — Utilización (SARIMAX)</h2>
  <p class="body">Filtra el universo a <code class="field">Segmento_Conductual == 'Revolver'</code>, agrupa por
  mes y calcula <code class="field">Saldo_Total</code>, <code class="field">Limite_Total</code> y
  <code class="field">Tasa_Utilizacion = Saldo_Total / Limite_Total</code>. Esta serie mensual se une con
  <code class="field">df_macro</code> por fecha.</p>
  <p class="body">El modelo estimado es un SARIMAX(1,1,1) con <code class="field">Y = Tasa_Utilizacion</code> y
  exógenas <code class="field">[ICC_Puntos, Masa_Salarial_Indice, Estacionalidad_Julio, Estacionalidad_Diciembre]</code>.
  El componente autorregresivo toma el rezago de un mes, la diferenciación de orden 1 remueve tendencia, y el
  componente de media móvil corrige el error de la proyección anterior. El output de esta etapa es la serie
  ajustada <code class="field">Utilizacion_Fitted</code>.</p>
</section>

<section class="blk">
  <h2 class="sec">Etapa 3 — Amortización (Logit + OLS)</h2>
  <p class="body">Sobre el mismo universo revolver, agrupa por fecha y calcula <code class="field">Pagos_Totales</code>,
  <code class="field">Saldo_Total</code> y <code class="field">Tasa_Pago_Mensual = Pagos_Totales / Saldo_Total</code>.
  Tras el merge con la base macro, transforma el objetivo con
  <code class="field">TPR_Logit = log(TPR / (1 - TPR + ε))</code> y construye
  <code class="field">Desempleo_Lag2 = Tasa_Desempleo_Pct.shift(2)</code>.</p>
  <p class="body">La regresión estimada es <code class="field">TPR_Logit ~ Spread_TC_PP + Desempleo_Lag2</code>
  por OLS. La predicción en escala logit se revierte a porcentaje con la función logística:
  <code class="field">TPR_Predicho = 1 / (1 + exp(-predicción_logit))</code>.</p>
</section>

<section class="blk">
  <h2 class="sec">Outputs reales</h2>
  <table class="io">
    <tr><th>Etapa</th><th>Variable</th><th>Qué representa</th></tr>
    <tr><td>Segmentación</td><td>Segmento_Conductual</td><td>Totalero / Revolver</td></tr>
    <tr><td>Utilización</td><td>Tasa_Utilizacion</td><td>Saldo usado sobre línea disponible, observado</td></tr>
    <tr><td>Utilización</td><td>Utilizacion_Fitted</td><td>Serie ajustada por el SARIMAX</td></tr>
    <tr><td>Amortización</td><td>Tasa_Pago_Mensual</td><td>Pagos sobre saldo, observado</td></tr>
    <tr><td>Amortización</td><td>TPR_Predicho</td><td>Tasa de pago proyectada por el modelo</td></tr>
  </table>
</section>

<section class="blk">
  <span class="notes-tag">Notas</span>
  <h2 class="sec">Consideraciones metodológicas</h2>
  <p class="body">El pipeline se apoya en un principio simple: no toda la cartera de tarjetas tiene el mismo
  comportamiento frente a tasas, y por lo tanto no puede modelarse como un bloque homogéneo. Antes de estimar
  cualquier serie de tiempo, el modelo separa qué parte del saldo tiene duración económica real y cuál no la
  tiene.</p>

  <h3 class="subsec">Segmentación conductual</h3>
  <p class="body">Un cliente que paga la totalidad de su saldo cada mes no genera duración económica que
  proyectar: su exposición se extingue dentro del mismo ciclo en que se originó. Incluir a estos clientes en la
  misma estimación que a los revolvers introduce ruido en la utilización y en la amortización, no porque el
  modelo esté mal especificado, sino porque el universo sobre el que se estima está mal definido. Esta
  clasificación es consistente con lo que SRP31 exige en materia de supuestos conductuales documentados.</p>

  <h3 class="subsec">Modelo de utilización</h3>
  <p class="body">El saldo absoluto de una cosecha nueva puede ser varios órdenes de magnitud mayor que el de
  una cosecha antigua, simplemente porque el banco colocó más tarjetas en ese período. Esto refleja crecimiento
  comercial, no un cambio en el comportamiento del producto. Por eso la variable modelada es la tasa de
  utilización y no el saldo: una proporción acotada entre 0 y 1, independiente del volumen de colocación.</p>

  <h3 class="subsec">Especificación SARIMAX (1,1,1)</h3>
  <p class="body">Es una especificación deliberadamente conservadora: con un número limitado de observaciones
  mensuales, una parametrización mayor incrementa el riesgo de sobreajuste antes de aportar poder explicativo
  adicional.</p>

  <h3 class="subsec">Modelo de amortización</h3>
  <p class="body">Spread_TC_PP y Desempleo_Lag2 representan dos mecanismos distintos de riesgo de
  comportamiento: el spread captura riesgo de opción, ya que un diferencial de tasas más alto incentiva al
  cliente a refinanciar o amortizar más rápido; el desempleo, con dos meses de rezago, captura deterioro de
  solvencia, que reduce la capacidad de pago independientemente de la voluntad del cliente.</p>

  <h3 class="subsec">Limitaciones actuales</h3>
  <p class="body">Con 72 observaciones mensuales y seis parámetros estimados, el SARIMAX presenta riesgo de
  sobreajuste, y en la corrida actual los componentes AR y MA no resultan estadísticamente significativos. Esto
  justifica probar alternativas más parsimoniosas, como ARIMA(0,1,1) o (1,1,0), antes de dar por definitiva la
  actual. De forma similar, cuando el coeficiente de ICC_Puntos resulta negativo, la explicación más probable es
  colinealidad con la masa salarial, y debería confirmarse con un análisis de VIF antes de descartar la
  variable.</p>

  <h3 class="subsec">Conclusión</h3>
  <p class="body">La solidez del pipeline no depende de que cada coeficiente resulte significativo en la corrida
  actual; eso se resuelve con más datos o una mejor especificación. Depende de que la secuencia de tres etapas
  —segmentación, utilización y amortización— refleje correctamente lo que SRP31 exige: supuestos conductuales
  documentados y consistentes con el comportamiento observado, previos a cualquier cálculo de ∆EVE.</p>
</section>
""", unsafe_allow_html=True)
