import { useEffect, useState } from "react";
import {
  ArrowDown,
  ArrowRight,
  ArrowUpRight,
  BadgeCheck,
  Check,
  CheckCircle2,
  CircleArrowRight,
  ClipboardCheck,
  Dna,
  FileText,
  FlaskConical,
  HeartPulse,
  LucideCaseUpper,
  Mail,
  Menu,
  Microscope,
  ShieldCheck,
  UsersRound,
  X,
} from "lucide-react";
import heroImage from "./images/HeroSection.png";
import contactImage from "./images/ConnectCTASection.png";
import labImage from "./images/Medical researcher using laboratory microscope.png";
import researchImage from "./images/Image (Researcher pipetting samples in a laboratory).png";
import neurosynImage from "./images/Container (7).png";
import pantosynImage from "./images/Container (8).png";
import trypsynImage from "./images/Container (9).png";
import cefixaImage from "./images/Container (10).png";
import betasynImage from "./images/Container (11).png";
import pregaImage from "./images/Container (12).png";
import pregaForteImage from "./images/Container (13).png";
import brandLogo from "./images/logo.png";
import qualityBackgroundImage from "./images/QualityCommitmentSection.png";

const productImages = {
  "neurosyn-m": neurosynImage,
  "pantosyn-20-40": pantosynImage,
  "trypsyn-r": trypsynImage,
  "cefixa-200": cefixaImage,
  "betasyn-8-16": betasynImage,
  pregasyn: pregaImage,
  "pregasyn-forte": pregaForteImage,
};

const neurosynDetails = {
  category: "Neurological Health",
  formulation: "RX PRESCRIPTION FORMULATION",
  name: "NEUROSYN-M™",
  composition: "Alpha Lipoic Acid 200 mg + Benfotiamine 100 mg + Folic Acid 1.5 mg + Inositol 100 mg + Methylcobalamin 1000 mcg + Vitamin B6 5 mg",
  facts: [
    ["Form & Pack", "Tablets • 10×10 Alu-Alu"],
    ["Indication Segment", "Neuropathy & Neuroprotection"],
    ["Shelf Life & Storage", "24 Mos • Below 25°C"],
    ["Compliance", "WHO-GMP Certified"],
  ],
  indications: [
    "Diabetic Peripheral Neuropathy",
    "Axon & Myelin Sheath Regeneration",
    "Neuronal Vascular & Metabolic Care",
    "Paresthesia & Hyperalgesia Relief",
  ],
  actives: [
    ["200 mg", "Alpha Lipoic Acid"],
    ["1000 mcg", "Methylcobalamin"],
    ["100 mg", "Benfotiamine"],
  ],
};

const initialProducts = [
  { id: "neurosyn-m", name: "Neurosyn-M", description: "Alpha Lipoic Acid 200 mg + Benfotiamine 100 mg + Folic Acid 1.5 mg + Inositol 100 mg + Methylcobalamin 1000 mcg + Vitamin B6 3 mg", category: "Neurological Health" },
  { id: "pantosyn-20-40", name: "Pantosyn 20/40", description: "Pantoprazole 20 mg / 40 mg Tablets", category: "Gastrointestinal Health" },
  { id: "trypsyn-r", name: "Trypsyn-R", description: "Bromelain 90 mg + Rutoside Trihydrate 100 mg + Trypsin 48 mg", category: "Musculoskeletal Support" },
  { id: "cefixa-200", name: "Cefixa 200", description: "Cefixime 200 mg Tablets", category: "Other Formulations" },
  { id: "betasyn-8-16", name: "Betasyn 8/16", description: "Betahistine 8 mg / 16 mg Tablets", category: "Other Formulations" },
  { id: "pregasyn", name: "Pregasyn", description: "Pregabalin 75 mg + Methylcobalamin 1500 mcg", category: "Neurological Health" },
  { id: "pregasyn-forte", name: "Pregasyn Forte", description: "Methylcobalamin 750 mcg + Pregabalin 50 mg", category: "Neurological Health" },
];

const emptyInquiryForm = { name: "", email: "", phone: "", company: "", topic: "", message: "" };

function formatProductCardName(product) {
  const name = product.name.toUpperCase();
  const trademarkPlacements = {
    "neurosyn-m": [/-M$/, "-M™"],
    "pantosyn-20-40": [/ 20\/40$/, "™ 20/40"],
    "trypsyn-r": [/-R$/, "-R™"],
    "cefixa-200": [/ 200$/, "™ 200"],
    "betasyn-8-16": [/ 8\/16$/, "™ 8/16"],
    pregasyn: [/$/, "™"],
    "pregasyn-forte": [/ FORTE$/, "™ FORTE"],
  };
  const placement = trademarkPlacements[product.id];
  return placement ? name.replace(placement[0], placement[1]) : `${name}™`;
}

const pointIcons = {
  quality: CircleArrowRight,
  transparency: FileText,
  standards: BadgeCheck,
  support: UsersRound,
  care: HeartPulse,
  clarity: ClipboardCheck,
  engagement: Dna,
};

const initialSiteContent = {
  nav_links: [
    { label: "Home", href: "#home" },
    { label: "About us", href: "#about" },
    { label: "products", href: "#products" },
    { label: "Why Choose Us", href: "#why-synexta" },
    { label: "Quality Assurance", href: "#quality" },
    { label: "Contact", href: "#contact" },
  ],
  nav_cta_label: "Explore Products",
  nav_cta_href: "#products",
  about_eyebrow: "ABOUT SYNEXTA PHARMA",
  about_title: "Committed to quality. Focused on care.",
  about_body: "Synexta Pharma offers a range of pharmaceutical formulations designed to support diverse healthcare needs. Our approach is built on quality, transparency and a genuine commitment to trusted healthcare solutions.",
  about_points: [
    { icon: "care", title: "Quality-Focused Approach", text: "Every Formulation is presented with care, clarity and consistency." },
    { icon: "clarity", title: "Reliable Pharmaceutical solutions", text: "A focused portfolio built around everyday healthcare needs." },
    { icon: "engagement", title: "Healthcare-Centered Commitment", text: "We work along side healthcare proffessionals for better patient care." },
  ],
  quality_eyebrow: "Quality Assurance",
  quality_points: [
    { icon: "quality", title: "Commitment to Quality", text: "Quality guides every product we bring to market." },
    { icon: "transparency", title: "Product Information Transparency", text: "Clear, accurate compositions for every formulation." },
    { icon: "standards", title: "Consistent Brand Standards", text: "A uniform standard of presentation across our range." },
    { icon: "support", title: "Healthcare Professional Support", text: "Responsive help for professionals and partners." },
  ],
  commitments_title: "OUR COMMITMENTS",
  commitments_subtitle: "Quality at the Heart of Every Formulation",
  commitments_points: [
    { icon: "quality", title: "Commitment to quality", text: "Quality guides every product we bring to market." },
    { icon: "transparency", title: "Product information transparency", text: "Clear, accurate compositions for every formulation." },
    { icon: "standards", title: "Consistent brand standards", text: "A uniform standard of presentation across our range." },
    { icon: "support", title: "Healthcare professional support", text: "Responsive help for professionals and partners." },
  ],
  why_eyebrow: "WHY CHOOSE US",
  why_title: "Why choose Synexta Pharma?",
  why_body: "We keep things simple: dependable products, clear information and a people-first approach.",
  why_points: [
    { icon: "care", title: "Quality first", text: "Formulation selevted and presented with a focus on quality." },
    { icon: "clarity", title: "Product Clarity", text: "Exact names, strengths and compositions- nothing hidden." },
    { icon: "engagement", title: "Responsible communication", text: "Accurate informationwithout exaggerated claims" },
    { icon: "engagement", title: "Proffessional Engagement", text: "A team that listens to healthcare proffessionals and partners" },
  ],
  footer_tagline: "Quality Medicines. Trusted Care.",
  footer_quick_links: [
    { label: "Home", href: "#home" },
    { label: "About Us", href: "#about" },
    { label: "Products", href: "#products" },
    { label: "Our Expertise", href: "#explore" },
    { label: "Quality Assurance", href: "#quality" },
    { label: "Contact", href: "#contact" },
  ],
  footer_products_heading: "Products",
  footer_product_links: [
    { label: "NEUROSYN-M™", href: "#contact" },
    { label: "TRYPSYN-R™", href: "#about" },
    { label: "BETASYN™ 8/16", href: "#about" },
    { label: "PREGASYN™", href: "#about" },
    { label: "PANTOSYN™ 20/40", href: "#contact" },
    { label: "CEFIXA™ 200", href: "#about" },
    { label: "PREGASYN™ FORTE", href: "#about" },
  ],
  footer_copyright: "© 2026 Synexta Pharma. All rights reserved.",
  footer_legal_links: [{ label: "Privacy Policy" }, { label: "Terms and Conditions" }],
};

function mergeSiteContent(data) {
  const content = { ...initialSiteContent, ...data };
  for (const field of [
    "nav_links",
    "about_points",
    "quality_points",
    "commitments_points",
    "why_points",
    "footer_quick_links",
    "footer_product_links",
    "footer_legal_links",
  ]) {
    content[field] = Array.isArray(data[field])
      ? data[field].filter((item) => item && typeof item === "object" && !Array.isArray(item))
      : initialSiteContent[field];
  }
  return content;
}

function SectionPoints({ points }) {
  return (
    <div className="difference-points">
      {points.map((point, index) => {
        const Icon = pointIcons[point.icon] || CircleArrowRight;
        return (
          <div className="difference-point" key={`${point.title || "point"}-${index}`}>
            <span className="difference-icon"><Icon size={18} /></span>
            <div><h3>{point.title}</h3><p>{point.text}</p></div>
          </div>
        );
      })}
    </div>
  );
}

function PrincipleCards({ points }) {
  return (
    <div className="principle-grid">
      {points.map((point, index) => {
        const Icon = pointIcons[point.icon] || CircleArrowRight;
        return (
          <article className="principle" key={`${point.title || "point"}-${index}`} tabIndex={0}>
            <span className="principle-icon"><Icon size={18} strokeWidth={2} /></span>
            <h3>{point.title}</h3>
            <p>{point.text}</p>
          </article>
        );
      })}
    </div>
  );
}

function Brand({ light = false, image = brandLogo }) {
  return (
    <a className={`brand${light ? " brand-light" : ""}`} href="#home" aria-label="Synexta Pharma home">
      <img className="brand-logo" src={image} alt="Synexta Pharma" />
    </a>
  );
}

function App() {
  const [products, setProducts] = useState(initialProducts);
  const [siteContent, setSiteContent] = useState(initialSiteContent);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [orderProduct, setOrderProduct] = useState(null);
  const [orderConfirmed, setOrderConfirmed] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState("delivery");
  const [menuOpen, setMenuOpen] = useState(false);
  const [formState, setFormState] = useState(emptyInquiryForm);
  const [submitState, setSubmitState] = useState({ status: "idle", message: "" });

  useEffect(() => {
    if (!selectedProduct && !orderProduct) return undefined;

    const closeOnEscape = (event) => {
      if (event.key === "Escape") {
        setSelectedProduct(null);
        setOrderProduct(null);
      }
    };
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", closeOnEscape);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", closeOnEscape);
    };
  }, [selectedProduct, orderProduct]);

  useEffect(() => {
    const controller = new AbortController();
    fetch("/api/content/", { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error("Website content is currently unavailable");
        return response.json();
      })
      .then((data) => setSiteContent(mergeSiteContent(data)))
      .catch((error) => {
        if (error.name !== "AbortError") console.info("Showing the default website content.");
      });
    return () => controller.abort();
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    fetch("/api/products/", { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error("Catalogue is currently unavailable");
        return response.json();
      })
      .then((data) => {
        if (Array.isArray(data.products)) setProducts(data.products);
      })
      .catch((error) => {
        if (error.name !== "AbortError") console.info("Showing the local product catalogue.");
      });
    return () => controller.abort();
  }, []);

  function chooseProduct(product) {
    setFormState((current) => ({ ...current, topic: `Product enquiry: ${product.name}` }));
    setSelectedProduct(null);
    document.querySelector("#contact")?.scrollIntoView({ behavior: "smooth" });
  }

  function startOrder(product) {
    setSelectedProduct(null);
    setPaymentMethod("delivery");
    setOrderConfirmed(false);
    setOrderProduct(product);
  }

  function updateField(event) {
    setFormState((current) => ({ ...current, [event.target.name]: event.target.value }));
    if (submitState.status !== "idle") setSubmitState({ status: "idle", message: "" });
  }

  async function submitInquiry(event) {
    event.preventDefault();
    setSubmitState({ status: "sending", message: "Sending your message..." });
    try {
      const response = await fetch("/api/contact/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formState),
      });
      const responseBody = await response.text();
      let data;
      if (!responseBody.trim()) {
        throw new Error(`The server returned an empty response (HTTP ${response.status}). Your enquiry was not confirmed.`);
      }
      try {
        data = JSON.parse(responseBody);
      } catch {
        throw new Error(`The server returned an invalid response (HTTP ${response.status}). Your enquiry was not confirmed.`);
      }
      if (!response.ok) {
        const detail = data && typeof data === "object"
          ? data.errors ? Object.values(data.errors).flat().join(" ") : data.error
          : "";
        throw new Error(detail || "We could not submit your message.");
      }
      if (!data || typeof data.message !== "string" || !data.message) {
        throw new Error("The server did not confirm your enquiry. Please try again.");
      }
      if (data.email_sent === false) {
        setSubmitState({ status: "warning", message: data.message });
        setFormState(emptyInquiryForm);
        return;
      }
      setSubmitState({ status: "success", message: data.message });
      setFormState(emptyInquiryForm);
    } catch (error) {
      setSubmitState({ status: "error", message: error.message || "Unable to reach the server. Please try again." });
    }
  }

  const closeMenu = () => setMenuOpen(false);

  return (
    <>
      <header className="site-header">
        <div className="header-inner">
          <Brand image={siteContent.logo_image || brandLogo} />
          <button className="menu-toggle" type="button" aria-label={menuOpen ? "Close navigation" : "Open navigation"} aria-expanded={menuOpen} onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? <X size={21} /> : <Menu size={21} />}
          </button>
          <nav className={`main-nav${menuOpen ? " is-open" : ""}`} aria-label="Main navigation">
            {siteContent.nav_links.map((link, index) => <a href={link.href} onClick={closeMenu} key={`${link.label}-${index}`}>{link.label}</a>)}
            <a className="nav-contact" href={siteContent.nav_cta_href} onClick={closeMenu}>{siteContent.nav_cta_label} <ArrowUpRight size={15} /></a>
          </nav>
        </div>
      </header>

      <main>
        <section className="hero" id="home" style={{ "--hero-image": `url("${siteContent.hero_image || heroImage}")` }}>
          <div className="hero-inner page-width">
            <div className="hero-copy">
              <span className="eyebrow hero-eyebrow"> TRUSTED PHARMACEUTICAL SOLUTIONS</span>
              <h1><span className="hero-heading-line">Quality medicines.</span><span>Trusted care.</span></h1>
              <p>Commited to delivering quality-driven pharmaceutical formulations that support healthcare proffessionals and better patient care.</p>
              <div className="hero-actions">
                <a className="button button-primary" href="#products">Explore our products <ArrowRight size={16} /></a>
                <a className="button button-quiet" href="#contact">Contact our team</a>
              </div>
            </div>
          </div>
          <div className="hero-index" aria-hidden="true">01 <span /> 04</div>
        </section>

        <section className="intro-section section-pad" id="about">
          <div className="intro-grid page-width">
            <div className="intro-image-wrap">
              <img src={siteContent.about_image || labImage} alt="Researcher working with a laboratory microscope" />
            </div>
            <div className="intro-copy">
              <span className="eyebrow">{siteContent.about_eyebrow}</span>
              <h2>{siteContent.about_title}</h2>
              <p className="body-lead">{siteContent.about_body}</p>
              <SectionPoints points={siteContent.about_points} />
              </div>
          </div>
        </section>

        <section className="products-section section-pad" id="products">
          <div className="page-width">
            <div className="section-heading">
              <span className="aqua">OUR PORTFOLIO</span>
              <h2>Our pharmaceutical products</h2>
              <p className="portfolio-description">Explore our range of pharmaceutical formulations developed to support diverse healthcare needs.</p>
            </div>
            <div className="product-grid">
              {products.map((product, index) => (
                <article className="product-card" key={product.id} style={{ "--card-index": index }}>
                  <div className="product-art">
                    {product.image || productImages[product.id] ? <img src={product.image || productImages[product.id]} alt={`${product.name} product pack`} /> : <div className="product-placeholder"><FlaskConical size={36} /></div>}
                  </div>
                  <div className="product-info">
                    <span className="product-category">{product.category || "Pharmaceuticals"}</span>
                    <h3>{formatProductCardName(product)}</h3>
                    <span className="product-accent-line" aria-hidden="true" />
                    <p>{product.description}</p>
                    <button className="product-link" type="button" onClick={() => setSelectedProduct(product)}>View Product <ArrowRight size={18} /></button>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="quality-section section-pad" id="quality" style={{ "--quality-background-image": `url("${siteContent.quality_background_image || qualityBackgroundImage}")` }}>
          <div className="page-width">
            <div className="section-heading section-heading-light">
              <span className="eyebrow">{siteContent.quality_eyebrow}</span>
            </div>
            <PrincipleCards points={siteContent.quality_points} />
          </div>
        </section>

        <section className="commitments-section section-pad" aria-labelledby="commitments-heading" style={{ "--quality-background-image": `url("${siteContent.quality_background_image || qualityBackgroundImage}")` }}>
          <div className="page-width">
            <h2 className="commitments-heading" id="commitments-heading">{siteContent.commitments_title}</h2>
            <h2 className="commitments-subheading">{siteContent.commitments_subtitle}</h2>
            <PrincipleCards points={siteContent.commitments_points} />
          </div>
        </section>

        <section className="difference-section section-pad" id="why-synexta">
          <div className="difference-grid page-width">
            <div className="difference-copy">
              <span className="eyebrow">{siteContent.why_eyebrow}</span>
              <h2>{siteContent.why_title}</h2>
              <p className="body-lead">{siteContent.why_body}</p>
              <SectionPoints points={siteContent.why_points} />
            </div>
            <div className="difference-image">
              <img src={siteContent.why_image || researchImage} alt="Scientist carefully pipetting a sample in a laboratory" />
            </div>
          </div>
        </section>

        <section className="contact-banner" style={{ "--contact-image": `url("${siteContent.contact_background_image || contactImage}")` }}>
          <div className="contact-banner-inner page-width">
            <span className="eyebrow">LET'S CONNECT</span>
            <h2>Let's Connect for Better Healthcare Solutions</h2>
            <p>Connect with our team to learn more about our pharmaceutical product portfolio and business enquiries.</p>
            <div className="contact-banner-actions">
              <a className="button button-primary" href="#contact">Contact Us <ArrowRight size={16} /></a>
              <a className="button button-quiet" href="#products">Explore Products</a>
            </div>
          </div>
        </section>

        <section className="contact-section section-pad" id="contact">
          <div className="contact-grid page-width">
            <div className="contact-copy">
              <span className="eyebrow">CONTACT</span>
              <h2>Get in touch.</h2>
              <p className="body-lead">Have a question about our products or a business enquiry? Send us a message and our team will get back to you.</p>
              <div className="contact-details">
                <div><span className="contact-detail-icon"><Mail size={17} /></span>Product Information request</div>
                <div><span className="contact-detail-icon"><Mail size={17} /></span>Distribution and business partnerships</div>
                <div><span className="contact-detail-icon"><Mail size={17} /></span>Healthcare proffessional support</div>
              </div>
            </div>
            <form className="contact-form" onSubmit={submitInquiry}>
              <div className="form-row">
                <label>Name<input name="name" autoComplete="name" placeholder="Your name" value={formState.name} onChange={updateField} required maxLength={120} /></label>
                <label>Business Email<input name="email" type="email" autoComplete="email" placeholder="you@example.com" value={formState.email} onChange={updateField} required maxLength={254} /></label>
              </div>
              <div className="form-row">
                <label>Phone Number <input name="phone" type="tel" autoComplete="tel" placeholder="+1 555 000 0000" value={formState.phone} onChange={updateField} maxLength={30} /></label>
                <label>Company/Organization<input name="company" placeholder="Company name" value={formState.company} onChange={updateField} required maxLength={120} /></label>
              </div>
              <label>Enquiry Type
                <select name="topic" value={formState.topic} onChange={updateField} required>
                  <option value="" disabled>Select an option</option>
                  {formState.topic.startsWith("Product enquiry:") && <option value={formState.topic}>{formState.topic}</option>}
                  <option value="Product Information request">Product Information request</option>
                  <option value="Distribution and business partnerships">Distribution and business partnerships</option>
                  <option value="Healthcare professional support">Healthcare professional support</option>
                  <option value="Other enquiry">Other enquiry</option>
                </select>
              </label>
              <label>Message<textarea name="message" placeholder="How can we help?" rows="4" value={formState.message} onChange={updateField} required minLength={10} maxLength={5000} /></label>
              <div className="form-submit-row">
                <p className={`form-feedback ${submitState.status}`} aria-live="polite">{submitState.message}</p>
                <button className="button button-primary submit-button" type="submit" disabled={submitState.status === "sending"}>
                  {submitState.status === "sending" ? "Sending..." : "Submit Enquiry"}<ArrowRight size={16} />
                </button>
              </div>
            </form>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div className="footer-main page-width">
          <div className="footer-brand"><Brand light image={siteContent.logo_image || brandLogo} /><p>{siteContent.footer_tagline}</p></div>
          <div className="footer-column"><span>Quick Links</span>{siteContent.footer_quick_links.map((link, index) => <a href={link.href} key={`${link.label}-${index}`}>{link.label}</a>)}</div>
          <div className="footer-products">
            <span>{siteContent.footer_products_heading}</span>
            <div className="footer-products-links">
              {siteContent.footer_product_links.map((link, index) => <a href={link.href} key={`${link.label}-${index}`}>{link.label}</a>)}
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>{siteContent.footer_copyright}</p>
          <div className="footer-legal">
            {siteContent.footer_legal_links.map((link, index) => link.href
              ? <a href={link.href} key={`${link.label}-${index}`}>{link.label}</a>
              : <span key={`${link.label}-${index}`}>{link.label}</span>)}
          </div>
        </div>
      </footer>
      {selectedProduct && !orderProduct && (
        <div className="product-dialog-backdrop" onMouseDown={(event) => {
          if (event.target === event.currentTarget) setSelectedProduct(null);
        }}>
          <section className="product-dialog" role="dialog" aria-modal="true" aria-labelledby="product-dialog-title">
            {selectedProduct.id === "neurosyn-m" ? (
              <>
                <header className="product-dialog-header">
                  <div className="product-dialog-tags">
                    <span>{neurosynDetails.category}</span>
                    <span>{neurosynDetails.formulation}</span>
                  </div>
                  <button className="product-dialog-close" type="button" aria-label="Close product details" autoFocus onClick={() => setSelectedProduct(null)}>
                    <X size={21} />
                  </button>
                  <h2 id="product-dialog-title">{neurosynDetails.name}</h2>
                  <p>{neurosynDetails.composition}</p>
                </header>
                <div className="product-dialog-content neurosyn-dialog-content">
                  <div className="product-dialog-overview">
                    <div className="product-dialog-image">
                      <img src={selectedProduct.image || productImages[selectedProduct.id]} alt={`${neurosynDetails.name} product pack`} />
                    </div>
                    <div className="product-dialog-facts">
                      {neurosynDetails.facts.map(([label, value]) => (
                        <div key={label}><span>{label}</span><strong>{value}</strong></div>
                      ))}
                    </div>
                  </div>
                  <section className="neurosyn-indications">
                    <h3>KEY THERAPEUTIC INDICATIONS</h3>
                    <ul>
                      {neurosynDetails.indications.map((indication) => (
                        <li key={indication}><FileText size={16} aria-hidden="true" />{indication}</li>
                      ))}
                    </ul>
                  </section>
                  <section className="neurosyn-actives">
                    <div className="neurosyn-actives-heading">
                      <h3>KEY ACTIVE ACTIVES</h3>
                      <span>Standardized Pharmacopoeial Grade</span>
                    </div>
                    <div className="neurosyn-actives-grid">
                      {neurosynDetails.actives.map(([amount, active]) => (
                        <div key={active}><strong>{amount}</strong><span>{active}</span></div>
                      ))}
                    </div>
                  </section>
                  <button className="button button-primary product-dialog-action" type="button" onClick={() => startOrder(selectedProduct)}>
                    Buy Now <ArrowRight size={16} />
                  </button>
                </div>
              </>
            ) : (
              <>
            <header className="product-dialog-header">
              <div className="product-dialog-tags">
                <span>{selectedProduct.category || "Pharmaceuticals"}</span>
                <span>Product information</span>
              </div>
              <button className="product-dialog-close" type="button" aria-label="Close product details" autoFocus onClick={() => setSelectedProduct(null)}>
                <X size={21} />
              </button>
              <h2 id="product-dialog-title">{selectedProduct.name}</h2>
              <p>{selectedProduct.description}</p>
            </header>
            <div className="product-dialog-content">
              <div className="product-dialog-overview">
                <div className="product-dialog-image">
                  {selectedProduct.image || productImages[selectedProduct.id]
                    ? <img src={selectedProduct.image || productImages[selectedProduct.id]} alt={`${selectedProduct.name} product pack`} />
                    : <FlaskConical size={54} aria-hidden="true" />}
                </div>
                <div className="product-dialog-facts">
                  <div><span>Category</span><strong>{selectedProduct.category || "Pharmaceuticals"}</strong></div>
                  <div><span>Product</span><strong>{selectedProduct.name}</strong></div>
                  <div><span>Product information</span><strong>Contact our team for details</strong></div>
                  <div><span>Use</span><strong>Refer to the product packaging and healthcare professional guidance</strong></div>
                </div>
              </div>
              <div className="product-dialog-description">
                <h3>PRODUCT DESCRIPTION</h3>
                <p>{selectedProduct.description}</p>
              </div>
              <button className="button button-primary product-dialog-action" type="button" onClick={() => chooseProduct(selectedProduct)}>
                Enquire About This Product <ArrowRight size={16} />
              </button>
            </div>
              </>
            )}
          </section>
        </div>
      )}
      {orderProduct && (
        <div className="product-dialog-backdrop" onMouseDown={(event) => {
          if (event.target === event.currentTarget) setOrderProduct(null);
        }}>
          <section className="product-dialog checkout-dialog" role="dialog" aria-modal="true" aria-labelledby="checkout-title">
            <header className="product-dialog-header">
              <button className="product-dialog-close" type="button" aria-label="Close checkout" autoFocus onClick={() => setOrderProduct(null)}>
                <X size={21} />
              </button>
              <div className="product-dialog-tags">
                <span>{orderConfirmed ? "Order status" : "Checkout"}</span>
                <span>{orderProduct.name}</span>
              </div>
              <h2 id="checkout-title">{orderConfirmed ? "Product ordered!" : "Choose a payment option"}</h2>
              <p>{orderConfirmed
                ? `${orderProduct.name} has been added to this demo order.`
                : `Select how you would like to pay for ${orderProduct.name}.`}</p>
            </header>
            <div className="product-dialog-content checkout-content">
              {orderConfirmed ? (
                <div className="checkout-confirmation" role="status">
                  <CheckCircle2 size={48} aria-hidden="true" />
                  <p>Your order is confirmed in this demo. No payment was collected and no order was sent to a pharmacy.</p>
                  <button className="button button-primary product-dialog-action" type="button" onClick={() => setOrderProduct(null)}>OK</button>
                </div>
              ) : (
                <>
                  <fieldset className="payment-options">
                    <legend>Payment method</legend>
                    <label className={paymentMethod === "delivery" ? "is-selected" : ""}>
                      <input type="radio" name="payment-method" value="delivery" checked={paymentMethod === "delivery"} onChange={() => setPaymentMethod("delivery")} />
                      <span><strong>Pay on delivery</strong><small>Pay when your order arrives</small></span>
                    </label>
                    <label className={paymentMethod === "online" ? "is-selected" : ""}>
                      <input type="radio" name="payment-method" value="online" checked={paymentMethod === "online"} onChange={() => setPaymentMethod("online")} />
                      <span><strong>Online payment</strong><small>Demo option — no payment will be taken</small></span>
                    </label>
                  </fieldset>
                  <p className="checkout-demo-note">Demo checkout only. Pressing OK will not process a payment or submit a real order.</p>
                  <button className="button button-primary product-dialog-action" type="button" onClick={() => setOrderConfirmed(true)}>
                    OK, place demo order <ArrowRight size={16} />
                  </button>
                </>
              )}
            </div>
          </section>
        </div>
      )}
    </>
  );
}

export default App;