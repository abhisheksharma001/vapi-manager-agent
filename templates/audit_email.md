# 📧 Professional Audit Failure Email

## Subject: [URGENT] Critical Audit Failure: {{assistant_name}}

## Body (High-End HTML)
```html
<!DOCTYPE html>
<html>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f9;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td style="padding: 20px 0 30px 0;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border: 1px solid #e1e4e8; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <!-- Header -->
                    <tr>
                        <td align="center" bgcolor="#d32f2f" style="padding: 40px 0 30px 0; color: #ffffff; font-size: 28px; font-weight: bold; letter-spacing: 1px;">
                            PERFORMANCE ALERT
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px 40px 30px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="color: #172b4d; font-size: 20px; font-weight: 600;">
                                        Critical Failure: {{assistant_name}}
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 20px 0 30px 0; color: #44546f; font-size: 16px; line-height: 24px;">
                                        An autonomous audit has flagged a performance rating of <span style="color: #d32f2f; font-weight: bold;">{{score}}/10</span>. Immediate intervention is recommended for the following call:
                                    </td>
                                </tr>
                                <!-- Metrics Table -->
                                <tr>
                                    <td>
                                        <table border="0" cellpadding="10" cellspacing="0" width="100%" style="background-color: #f8f9fa; border-radius: 6px;">
                                            <tr>
                                                <td width="30%" style="color: #6b778c; font-weight: 600; font-size: 13px;">CALL ID</td>
                                                <td style="color: #172b4d; font-family: monospace; font-size: 14px;">{{call_id}}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #6b778c; font-weight: 600; font-size: 13px;">TIMESTAMP</td>
                                                <td style="color: #172b4d; font-size: 14px;">{{call_time}}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <!-- Reasons -->
                                <tr>
                                    <td style="padding: 30px 0 10px 0; color: #172b4d; font-size: 18px; font-weight: 600;">
                                        Failure Analysis
                                    </td>
                                </tr>
                                <tr>
                                    <td style="color: #44546f; font-size: 15px; line-height: 22px;">
                                        <ul style="padding-left: 20px; margin: 0;">
                                            {{#each reasons}}
                                            <li style="margin-bottom: 8px;">{{this}}</li>
                                            {{/each}}
                                        </ul>
                                    </td>
                                </tr>
                                <!-- Transcript -->
                                <tr>
                                    <td style="padding: 30px 0 0 0;">
                                        <div style="background-color: #fff4f4; border-left: 4px solid #d32f2f; padding: 20px; border-radius: 4px;">
                                            <p style="margin: 0 0 10px 0; font-weight: 700; color: #d32f2f; font-size: 14px; text-transform: uppercase;">Transcript Evidence</p>
                                            <p style="margin: 0; color: #172b4d; font-style: italic; font-size: 15px;">"{{actual_response}}"</p>
                                        </div>
                                    </td>
                                </tr>
                                <!-- CTA -->
                                <tr>
                                    <td align="center" style="padding: 40px 0 0 0;">
                                        <a href="{{recording_url}}" style="background-color: #0052cc; color: #ffffff; padding: 14px 30px; text-decoration: none; border-radius: 4px; font-weight: 600; font-size: 16px;">Review Call Recording</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td bgcolor="#f4f5f7" style="padding: 30px 30px 30px 30px; color: #6b778c; font-size: 12px; text-align: center; line-height: 18px;">
                            Sent autonomously by Ellavox Manager (OpenClaw POC)<br>
                            Streak Status: <span style="font-weight: bold;">{{streak_count}} ({{streak_type}})</span>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```
