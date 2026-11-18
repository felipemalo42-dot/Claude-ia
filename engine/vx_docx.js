// Genera GUION_COMPLETO.docx a partir del JSON que exporta vx_package.py.
// Uso: node vx_docx.js guion.json salida.docx
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, PageOrientation, BorderStyle, LevelFormat, Footer, PageNumber, TableLayoutType,
} = require("docx");

const data = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const out = process.argv[3];
const FONT = "Arial";
const C = { ink: "1A1A1A", rosa: "C2185B", gris: "666666", verde: "1E7B45", ambar: "A86400", fondo: "F6F1E9", cab: "2B1B3D" };

function runs(parts, base = {}) {
  // parts: [{t, b, i, color}]
  return parts.map((p) => new TextRun({ text: p.t, bold: !!p.b, italics: !!p.i, color: p.color || base.color || C.ink, size: p.size || base.size || 20, font: FONT }));
}
function P(parts, opts = {}) {
  if (typeof parts === "string") parts = [{ t: parts }];
  return new Paragraph({ children: runs(parts, opts), spacing: { before: opts.before ?? 0, after: opts.after ?? 80 }, alignment: opts.align, keepNext: opts.keepNext });
}
function H(text, level) {
  return new Paragraph({ heading: level, children: [new TextRun({ text, font: FONT })] });
}
const PAGE_W = 16838, PAGE_H = 11906, MARGIN = 900; // A4 apaisado (DXA)
const TABLE_W = PAGE_W - 2 * MARGIN;
const COLS = [1150, 6600, 4850, TABLE_W - 1150 - 6600 - 4850];

function cell(children, width, fill) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: fill ? { type: ShadingType.CLEAR, color: "auto", fill } : undefined,
    margins: { top: 70, bottom: 70, left: 100, right: 100 },
    children,
  });
}
function headerRow() {
  const labels = ["Tiempo", "Narración (negrita = énfasis · [pausa])", "Visual y sonido", "Ritmo"];
  return new TableRow({ tableHeader: true, children: labels.map((l, i) => cell([P([{ t: l, b: true, color: "FFFFFF" }], { after: 0 })], COLS[i], C.cab)) });
}
function sectionRow(title) {
  return new TableRow({ children: [new TableCell({ columnSpan: 4, width: { size: TABLE_W, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, color: "auto", fill: "F3D9E4" },
    margins: { top: 60, bottom: 60, left: 100, right: 100 }, children: [P([{ t: title, b: true, color: C.rosa, size: 22 }], { after: 0 })] })] });
}

const rows = [headerRow()];
for (const b of data.beats) {
  if (b.section) rows.push(sectionRow(b.section));
  const narr = b.lines.length ? b.lines.map((ln) => P(ln.parts.concat(ln.pause ? [{ t: `  [pausa ${ln.pause}]`, i: true, color: C.gris }] : []), { after: 60 })) : [P([{ t: b.silent, i: true, color: C.gris }])];
  const vis = [P([{ t: b.visual || "", size: 18 }], { after: 40 })];
  if (b.sfx) vis.push(P([{ t: "Sonido: ", b: true, size: 18 }, { t: b.sfx, size: 18, color: C.gris }], { after: 40 }));
  if (b.music) vis.push(P([{ t: "Música: ", b: true, size: 18 }, { t: b.music, size: 18, color: C.gris }], { after: 40 }));
  if (b.cert) vis.push(P([{ t: b.cert, b: true, size: 18, color: b.cert.startsWith("INTERPRET") ? C.ambar : C.verde }], { after: 0 }));
  rows.push(new TableRow({ cantSplit: false, children: [
    cell([P([{ t: b.time, b: true }], { after: 0 }), P([{ t: b.dur, color: C.gris, size: 16 }], { after: 0 })], COLS[0]),
    cell(narr, COLS[1]), cell(vis, COLS[2]), cell([P([{ t: b.ritmo || "", size: 18 }], { after: 0 })], COLS[3], C.fondo),
  ] }));
}
const scriptTable = new Table({ width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: COLS, layout: TableLayoutType.FIXED, rows });

const bullets = { reference: "vinetas", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 260 } } } }] };
const li = (parts) => new Paragraph({ numbering: { reference: "vinetas", level: 0 }, children: runs(typeof parts === "string" ? [{ t: parts }] : parts), spacing: { after: 60 } });

const ficha = data.ficha.map(([k, v]) => new TableRow({ children: [
  cell([P([{ t: k, b: true }], { after: 0 })], 3600, "F3EEF8"), cell([P(v, { after: 0 })], TABLE_W - 3600),
] }));

const children = [
  new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun({ text: data.title, font: FONT })] }),
  P([{ t: data.subtitle, i: true, color: C.gris, size: 24 }], { after: 200 }),
  H("Ficha de producción", HeadingLevel.HEADING_1),
  new Table({ width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: [3600, TABLE_W - 3600], rows: ficha }),
  H("Cómo leer este guion", HeadingLevel.HEADING_1),
  li([{ t: "Negrita", b: true }, { t: ": palabras que la narradora remarca." }]),
  li([{ t: "[pausa 0,4 s]", i: true, color: C.gris }, { t: ": silencio medido en la versión final (incluye las pausas naturales de la voz)." }]),
  li([{ t: "DOCUMENTADO / OFICIAL", b: true, color: C.verde }, { t: " (verde) y " }, { t: "INTERPRETACIÓN", b: true, color: C.ambar }, { t: " (amarillo): semáforo de certeza que aparece en pantalla." }]),
  li("Tiempos: inicio de cada bloque en el video final (mm:ss), medidos sobre la narración real."),
  H("Guion con marcas de tiempo", HeadingLevel.HEADING_1),
  scriptTable,
  H("Fuentes por capítulo", HeadingLevel.HEADING_1),
  ...data.sources.flatMap(([sec, srcs]) => [P([{ t: sec, b: true, color: C.rosa }], { before: 120, after: 40, keepNext: true }), ...srcs.map((s) => li(s))]),
  H("Grabar la narración con voz humana", HeadingLevel.HEADING_1),
  ...data.human.map((t) => li(t)),
  H("Narración completa (texto corrido)", HeadingLevel.HEADING_1),
  ...data.plain.map((t) => P(t, { after: 120 })),
];

const doc = new Document({
  creator: "Sal y Asfalto", title: data.title,
  styles: {
    default: { document: { run: { font: FONT, size: 20 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { font: FONT, size: 44, bold: true, color: C.cab }, paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONT, size: 30, bold: true, color: C.rosa }, paragraph: { spacing: { before: 320, after: 140 }, keepNext: true, outlineLevel: 0 } },
    ],
  },
  numbering: { config: [bullets] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Sal y Asfalto · Guion VIDEO_EXTRA · página ", font: FONT, size: 16, color: C.gris }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: C.gris })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(out, buf); console.log("docx listo:", out); });
