import { NextRequest, NextResponse } from "next/server";

type ContactBody = {
  name: string;
  email: string;
  phone?: string;
  social?: string;
  projectType?: string;
  message: string;
};

const rateMap = new Map<string, { count: number; reset: number }>();
const RATE_LIMIT = 5;
const RATE_WINDOW_MS = 60 * 60 * 1000;

function checkRate(ip: string): boolean {
  const now = Date.now();
  const entry = rateMap.get(ip);
  if (!entry || now > entry.reset) {
    rateMap.set(ip, { count: 1, reset: now + RATE_WINDOW_MS });
    return true;
  }
  if (entry.count >= RATE_LIMIT) return false;
  entry.count += 1;
  return true;
}

function escapeHtml(str: string) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function isValidEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validate(body: unknown): { ok: true; data: ContactBody } | { ok: false; error: string } {
  if (!body || typeof body !== "object") {
    return { ok: false, error: "Invalid form data." };
  }
  const b = body as Record<string, unknown>;
  const name = String(b.name ?? "").trim();
  const email = String(b.email ?? "").trim();
  const message = String(b.message ?? "").trim();
  const phone = String(b.phone ?? "").trim().slice(0, 30);
  const social = String(b.social ?? "").trim().slice(0, 200);
  const projectType = String(b.projectType ?? "").trim().slice(0, 50);

  if (!name || name.length > 100) return { ok: false, error: "Please provide a valid name." };
  if (!email || !isValidEmail(email) || email.length > 150)
    return { ok: false, error: "Please provide a valid email." };
  if (!message || message.length > 2000)
    return { ok: false, error: "Please provide a message." };

  return {
    ok: true,
    data: { name, email, phone, social, projectType, message },
  };
}

export async function POST(req: NextRequest) {
  try {
    const ip =
      req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ||
      req.headers.get("x-real-ip") ||
      "unknown";

    if (!checkRate(ip)) {
      return NextResponse.json(
        { error: "Too many requests. Please try again later." },
        { status: 429 }
      );
    }

    let body: unknown;
    try {
      body = await req.json();
    } catch {
      return NextResponse.json({ error: "Invalid JSON." }, { status: 400 });
    }

    const result = validate(body);
    if (!result.ok) {
      return NextResponse.json({ error: result.error }, { status: 400 });
    }

    const data = result.data;
    const timestamp = new Date().toISOString();

    const html = `
      <h2>New Website Inquiry</h2>
      <p><strong>Name:</strong> ${escapeHtml(data.name)}</p>
      <p><strong>Email:</strong> ${escapeHtml(data.email)}</p>
      <p><strong>WhatsApp:</strong> ${escapeHtml(data.phone || "—")}</p>
      <p><strong>Project Type:</strong> ${escapeHtml(data.projectType || "—")}</p>
      <p><strong>YouTube/Social:</strong> ${escapeHtml(data.social || "—")}</p>
      <p><strong>Message:</strong></p>
      <p>${escapeHtml(data.message).replace(/\n/g, "<br>")}</p>
      <p><strong>Timestamp:</strong> ${timestamp}</p>
    `;

    const text = `
New Website Inquiry

Name: ${data.name}
Email: ${data.email}
WhatsApp: ${data.phone || "—"}
Project Type: ${data.projectType || "—"}
YouTube/Social: ${data.social || "—"}
Message:
${data.message}

Timestamp: ${timestamp}
    `.trim();

    const host = process.env.SMTP_HOST;
    const user = process.env.SMTP_USER;
    const pass = process.env.SMTP_PASS;
    const to = process.env.CONTACT_TO || "chauhannilay888@gmail.com";
    const from = process.env.SMTP_FROM || user || "noreply@editforge.local";

    if (!host || !user || !pass) {
      console.error("SMTP not configured. Set SMTP_HOST, SMTP_USER, SMTP_PASS in .env.local");
      if (process.env.NODE_ENV !== "production") {
        console.log("[DEV] Contact form payload:", data);
        return NextResponse.json({ ok: true, dev: true });
      }
      return NextResponse.json(
        {
          error:
            "Contact form is temporarily unavailable. Please email or WhatsApp me directly.",
        },
        { status: 503 }
      );
    }

    let nodemailer: typeof import("nodemailer");
    try {
      nodemailer = await import("nodemailer");
    } catch {
      console.error("nodemailer package not installed — run: npm install nodemailer");
      return NextResponse.json(
        {
          error:
            "Contact form is temporarily unavailable. Please email or WhatsApp me directly.",
        },
        { status: 503 }
      );
    }

    const transporter = nodemailer.createTransport({
      host,
      port: Number(process.env.SMTP_PORT || 587),
      secure: process.env.SMTP_SECURE === "true",
      auth: { user, pass },
    });

    await transporter.sendMail({
      from: `"EditForge Portfolio" <${from}>`,
      to,
      replyTo: data.email,
      subject: `New inquiry from ${data.name}`,
      text,
      html,
    });

    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("Contact API error:", err);
    return NextResponse.json(
      {
        error:
          "Something went wrong while sending your message. Please try again or contact me directly by email/WhatsApp.",
      },
      { status: 500 }
    );
  }
}
