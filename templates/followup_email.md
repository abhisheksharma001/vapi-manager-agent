# 📧 Professional Follow-Up Alert

## Subject: [FOLLOW-UP] Minor Deviation: {{assistant_name}} (Streak: {{streak_count}})

## Body (High-End Minimal HTML)
```html
<!DOCTYPE html>
<html>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #ffffff;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td style="padding: 10px 0;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="550" style="border-collapse: collapse; border: 1px solid #ffccbc; background-color: #fffbf9; border-radius: 6px;">
                    <!-- Minimal Header -->
                    <tr>
                        <td bgcolor="#fff3e0" style="padding: 15px 20px; color: #e64a19; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #ffccbc;">
                            Action Recommended: Minor Guideline Deviation
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 25px 20px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td style="color: #172b4d; font-size: 18px; font-weight: 600; padding-bottom: 10px;">
                                        Assistant: {{assistant_name}}
                                    </td>
                                </tr>
                                <tr>
                                    <td style="color: #44546f; font-size: 15px; line-height: 22px; padding-bottom: 20px;">
                                        The recent call with ID <strong>{{call_id}}</strong> showed a minor procedural error: <br>
                                        <span style="color: #172b4d; font-style: italic;">"{{reason}}"</span>
                                    </td>
                                </tr>
                                <!-- Quick Link -->
                                <tr>
                                    <td>
                                        <a href="{{recording_url}}" style="display: inline-block; background-color: #1a73e8; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: 600; font-size: 14px;">Review Call Recording</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Minimal Footer -->
                    <tr>
                        <td style="padding: 15px 20px; border-top: 1px solid #ffccbc; color: #7a869a; font-size: 11px;">
                            <strong>Current Streak:</strong> {{streak_count}} ({{streak_type}}) | Monitoring via Ellavox Manager
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```
