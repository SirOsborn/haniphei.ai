import { jsPDF } from "jspdf";

const renderTextWithHighlight = (doc, text, highlight, x, y, maxWidth, lineH) => {
  const lines = doc.splitTextToSize(text, maxWidth);
  const hlWords = new Set(
    (highlight || "")
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, "")
      .split(/\s+/)
      .filter((w) => w.length > 3)
  );
  lines.forEach((line) => {
    const isHighlighted = hlWords.size > 0 && [...hlWords].some((w) => line.toLowerCase().includes(w));
    if (isHighlighted) {
      // Yellow highlight background
      const lw = doc.getTextWidth(line);
      doc.setFillColor(255, 235, 59);
      doc.rect(x - 1, y - lineH + 1.5, lw + 2, lineH, "F");
      doc.setTextColor(30, 20, 0);
      doc.setFont("helvetica", "bold");
    } else {
      doc.setTextColor(40, 40, 60);
      doc.setFont("helvetica", "normal");
    }
    doc.text(line, x, y);
    y += lineH;
  });
  return y;
};

export const exportToPDF = ({ findings, riskDetails, documentType = "Document" }) => {
  const doc = new jsPDF({ unit: "mm", format: "a4" });
  const W = doc.internal.pageSize.getWidth();
  const H = doc.internal.pageSize.getHeight();
  const margin = 20;
  const contentW = W - margin * 2;
  const lineH = 5.5;

  const detectedFindings = findings.filter((f) => f.count > 0 && riskDetails[f.id]);

  const fillWhite = () => {
    doc.setFillColor(255, 255, 255);
    doc.rect(0, 0, W, H, "F");
  };
  const addPage = () => { doc.addPage(); fillWhite(); };

  fillWhite();

  // ── Header bar ────────────────────────────────────────────────────────────
  doc.setFillColor(99, 102, 241);
  doc.rect(0, 0, W, 14, "F");

  doc.setFont("helvetica", "bold");
  doc.setFontSize(11);
  doc.setTextColor(255, 255, 255);
  doc.text("Haniphei.ai  —  Risk Analysis Report", margin, 9);

  const date = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
  doc.setFont("helvetica", "normal");
  doc.setFontSize(8);
  doc.text(`${documentType}  ·  ${date}`, W - margin, 9, { align: "right" });

  // ── Legend ────────────────────────────────────────────────────────────────
  let y = 24;
  doc.setFillColor(255, 235, 59);
  doc.rect(margin, y - 3.5, 7, 5, "F");
  doc.setFont("helvetica", "normal");
  doc.setFontSize(8);
  doc.setTextColor(100, 100, 130);
  doc.text("= Identified risk phrase", margin + 9, y);
  y += 9;

  // ── Findings ──────────────────────────────────────────────────────────────
  detectedFindings.forEach((finding, fi) => {
    const detail = riskDetails[finding.id];
    const lvl = (detail.riskLevel || "").toLowerCase();
    const riskCol  = lvl.includes("high") ? [220, 38, 38]  : lvl.includes("medium") ? [217, 119, 6]  : [22, 163, 74];
    const riskBgFill = lvl.includes("high") ? [254, 226, 226] : lvl.includes("medium") ? [254, 243, 199] : [220, 252, 231];

    if (fi > 0) {
      y += 4;
      doc.setDrawColor(220, 220, 235);
      doc.setLineWidth(0.3);
      doc.line(margin, y, W - margin, y);
      y += 6;
    }
    if (y > H - 40) { addPage(); y = 22; }

    // Risk badge
    doc.setFillColor(...riskBgFill);
    doc.roundedRect(margin, y - 4, 34, 6, 2, 2, "F");
    doc.setFont("helvetica", "bold");
    doc.setFontSize(7);
    doc.setTextColor(...riskCol);
    doc.text(detail.riskLevel.toUpperCase(), margin + 3, y + 0.2);

    // Section label (right)
    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    doc.setTextColor(150, 150, 180);
    doc.text(detail.excerpts?.[0]?.section || "", W - margin, y + 0.2, { align: "right" });
    y += 8;

    // Title
    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.setTextColor(20, 20, 40);
    doc.text(detail.title, margin, y);
    y += 7;

    // Excerpt blocks
    (detail.excerpts || []).forEach((excerpt) => {
      const textLines = doc.splitTextToSize(excerpt.text || "", contentW - 8);
      const blockH = textLines.length * lineH + 10;
      if (y + blockH > H - 20) { addPage(); y = 22; }

      // Light grey card
      doc.setFillColor(248, 248, 252);
      doc.roundedRect(margin, y - 2, contentW, blockH, 3, 3, "F");

      // Left accent bar
      doc.setFillColor(...riskCol);
      doc.roundedRect(margin, y - 2, 2.5, blockH, 1, 1, "F");

      doc.setFontSize(8.5);
      y = renderTextWithHighlight(
        doc, excerpt.text || "", excerpt.highlight || "",
        margin + 6, y + 5, contentW - 10, lineH
      );
      y += 6;
    });
  });

  // ── Footer ────────────────────────────────────────────────────────────────
  const totalPages = doc.getNumberOfPages();
  for (let p = 1; p <= totalPages; p++) {
    doc.setPage(p);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(7.5);
    doc.setTextColor(160, 160, 190);
    doc.text(
      "Your documents are processed securely. We never store or share your data.",
      W / 2, H - 7, { align: "center" }
    );
    doc.setDrawColor(220, 220, 235);
    doc.setLineWidth(0.3);
    doc.line(margin, H - 11, W - margin, H - 11);
  }

  const dateStr = new Date().toISOString().split("T")[0];
  doc.save(`Haniphei-Risk-Report-${dateStr}.pdf`);
};
