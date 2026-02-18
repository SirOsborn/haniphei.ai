export const findings = [
  { id: 1, category: "Hidden Financial Risk", count: 1 },
  { id: 2, category: "Unfair Obligation", count: 0 },
  { id: 3, category: "Termination & Exist Risk", count: 1 },
  { id: 4, category: "Ambiguous or Vague Language", count: 1 },
  { id: 5, category: "Legal Protection Gaps", count: 1 },
  { id: 6, category: "Suspicious or Buried Clauses", count: 0 },
];

export const riskDetails = {
  1: {
    title: "Hidden Financial Risk",
    riskLevel: "High Risk",
    description:
      "The contract contains clauses that may impose unexpected financial obligations or penalties that are not immediately apparent.",
    excerpts: [
      {
        text: "In the event of early termination by the Client, the Client shall be liable for all fees that would have been payable for the remainder of the contract term, plus a penalty fee equal to 25% of such remaining fees. Additionally, the Client agrees to reimburse the Company for any third-party costs incurred, including but not limited to subcontractor fees, licensing costs, and administrative expenses.",
        highlight:
          "shall be liable for all fees that would have been payable for the remainder of the contract term, plus a penalty fee equal to 25%",
        section: "Section 4.2: Termination Penalties",
      },
    ],
  },
  3: {
    title: "Termination & Exit Risk",
    riskLevel: "Medium Risk",
    description:
      "Restrictive termination clauses that may limit your ability to exit the agreement or impose significant penalties for early termination.",
    excerpts: [
      {
        text: "Either party may terminate this Agreement upon ninety (90) days written notice. However, Client must provide written justification deemed acceptable by the Company. The Company reserves the right to reject termination requests that do not meet criteria outlined in Appendix C (not included in this document).",
        highlight:
          "Client must provide written justification deemed acceptable by the Company. The Company reserves the right to reject termination requests",
        section: "Section 4.1: Termination Conditions",
      },
    ],
  },
  4: {
    title: "Ambiguous or Vague Language",
    riskLevel: "Low Risk",
    description:
      "Unclear language or undefined terms that could lead to different interpretations and potential disputes.",
    excerpts: [
      {
        text: "The Company will deliver services in a timely manner according to industry standards. All deliverables shall meet reasonable quality expectations. The Client agrees that timelines may be adjusted as necessary to ensure optimal results.",
        highlight:
          "timely manner according to industry standards... reasonable quality expectations... adjusted as necessary",
        section: "Section 2.3: Service Delivery Standards",
      },
    ],
  },
  5: {
    title: "Legal Protection Gaps",
    riskLevel: "Medium Risk",
    description:
      "Missing or inadequate legal protections that may leave you vulnerable in case of disputes or contract breaches.",
    excerpts: [
      {
        text: "The Company provides services 'as is' and makes no warranties, express or implied, regarding the services or deliverables. The Company's liability is limited to the fees paid in the preceding three (3) months. The Company shall not be liable for any indirect, incidental, or consequential damages.",
        highlight:
          "services 'as is' and makes no warranties... shall not be liable for any indirect, incidental, or consequential damages",
        section: "Section 7: Limitation of Liability",
      },
    ],
  },
};
