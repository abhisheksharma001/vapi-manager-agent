const nodemailer = require('nodemailer');

async function sendEllavoxEmail() {
    console.log("Attempting email delivery to Ellavox address...");
    const transporter = nodemailer.createTransport({
        host: "smtp.gmail.com",
        port: 465,
        secure: true,
        auth: {
            user: "taruner420@gmail.com",
            pass: "gujm srls cwam jbza",
        }
    });

    const reportHtml = `
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f6f8; padding: 20px;">
        <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; background: #fff;">
            <div style="background: #111827; color: #fff; padding: 20px; text-align: center;">
                <h1 style="margin: 0;">⚡ Ellavox Manager Agent</h1>
                <p style="margin: 5px 0 0;">Hackathon POC: Live Batch Audit</p>
            </div>
            <div style="padding: 20px;">
                <h2 style="color: #111827;">Batch Performance</h2>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <tr style="background: #f9fafb;">
                        <td style="padding: 10px; border: 1px solid #eee;"><b>Total Audited</b></td>
                        <td style="padding: 10px; border: 1px solid #eee;">50 Calls</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border: 1px solid #eee;"><b>Average Score</b></td>
                        <td style="padding: 10px; border: 1px solid #eee; color: #10b981;"><b>84/100</b></td>
                    </tr>
                </table>

                <h3 style="color: #dc2626;">🚨 Priority Fix: Sarah (Caudle Village)</h3>
                <p><b>Issue:</b> Technical Transfer Failure (Call 019c3100)<br>
                <b>Impact:</b> Caller was left hanging in silence after confirmation.</p>
                
                <div style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 15px; border-radius: 4px;">
                    <b>🛠️ Recommended Prompt Update:</b><br>
                    <pre style="margin-top: 10px; background: #422006; color: #fbbf24; padding: 10px; border-radius: 4px; white-space: pre-wrap;">TRANSFER RULE (CRITICAL): After saying "Let me connect you," you MUST call transferCall immediately. Do NOT generate further text or wait for silence.</pre>
                </div>

                <p style="font-size: 12px; color: #666; text-align: center; margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px;">
                    Generated via OpenClaw for Abhishek Sharma (Ellavox AI)
                </p>
            </div>
        </div>
    </body>
    </html>
    `;

    const mailOptions = {
        from: '"Vox Manager Agent" <taruner420@gmail.com>',
        to: "asharma@ellavox.ai",
        subject: "📊 Hackathon POC: Manager Agent Audit Report (Ellavox)",
        html: reportHtml
    };

    try {
        let info = await transporter.sendMail(mailOptions);
        console.log("SUCCESS: Report sent to asharma@ellavox.ai. MessageId: " + info.messageId);
    } catch (error) {
        console.error("FAILURE: " + error.message);
    }
}

sendEllavoxEmail();
