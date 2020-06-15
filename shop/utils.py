import time
import os

from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

import smtplib

from email.message import EmailMessage


def generate_and_send_pdf_for_invoice(request, invoice_id=None):

    # Generate pdf
    font_config = FontConfiguration()
    if invoice_id is not None:
        invoice_items = request.user.invoices.get(id=invoice_id).items.all()
    else:
        invoice_items = request.user.invoices.sorted_by('-created_at').first().items.all()

    items_block = """"""
    total_price = 0

    for invoice_item in invoice_items:
        items_block += f"""
            <tr class="item">
                <td>
                    {invoice_item.item.name}
                </td>
                
                <td>
                    {invoice_item.count}
                </td>
                
                <td>
                    ${float(invoice_item.fixed_price) * float(invoice_item.count)}
                </td>
            </tr>
        """

        total_price += float(invoice_item.fixed_price) * float(invoice_item.count)

    html_template = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>A simple, clean, and responsive HTML invoice template</title>
    </head>
    <body>
        <div class="invoice-box">
            <table cellpadding="0" cellspacing="0">
                <tr class="top">
                    <td colspan="3">
                        <table>
                            <tr>
                                <td class="title">
                                    <img src="https://www.sparksuite.com/images/logo.png" style="width:100%; max-width:300px;">
                                </td>
                                
                                <td>
                                    Invoice #: 123<br>
                                    Created: January 1, 2015<br>
                                    Due: February 1, 2015
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                
                <tr class="information">
                    <td colspan="3">
                        <table>
                            <tr>
                                <td>
                                    Sparksuite, Inc.<br>
                                    12345 Sunny Road<br>
                                    Sunnyville, CA 12345
                                </td>
                                
                                <td>
                                    Acme Corp.<br>
                                    John Doe<br>
                                    john@example.com
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                
                <tr class="heading">
                    <td>
                        Payment Method
                    </td>
                    
                    <td>
                        
                    </td>

                    <td>
                        Check #
                    </td>
                </tr>
                
                <tr class="details">
                    <td>
                        Check
                    </td>
                    
                    <td>
                        
                    </td>

                    <td>
                        1000
                    </td>
                </tr>
                
                <tr class="heading">
                    <td>
                        Item
                    </td>
                    
                    <td>
                        Count
                    </td>
                    
                    <td>
                        Price
                    </td>
                </tr>
                
                {items_block}
                
                <tr class="total">
                    <td></td>
                    
                    <td>
                       Total: ${total_price}
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """

    html = HTML(string=html_template)

    css = CSS(string='''
            .invoice-box {
            max-width: 800px;
            margin: auto;
            padding: 30px;
            border: 1px solid #eee;
            box-shadow: 0 0 10px rgba(0, 0, 0, .15);
            font-size: 16px;
            line-height: 24px;
            font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
            color: #555;
        }
        
        .invoice-box table {
            width: 100%;
            line-height: inherit;
            text-align: left;
        }
        
        .invoice-box table td {
            padding: 5px;
            vertical-align: top;
        }
        
        .invoice-box table tr td:nth-child(2) {
            text-align: right;
        }
        
        .invoice-box table tr.top table td {
            padding-bottom: 20px;
        }
        
        .invoice-box table tr.top table td.title {
            font-size: 45px;
            line-height: 45px;
            color: #333;
        }
        
        .invoice-box table tr.information table td {
            padding-bottom: 40px;
        }
        
        .invoice-box table tr.heading td {
            background: #eee;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
        }
        
        .invoice-box table tr.details td {
            padding-bottom: 20px;
        }
        
        .invoice-box table tr.item td{
            border-bottom: 1px solid #eee;
        }
        
        .invoice-box table tr.item.last td {
            border-bottom: none;
        }
        
        .invoice-box table tr.total td:nth-child(2) {
            border-top: 2px solid #eee;
            font-weight: bold;
        }
        
        @media only screen and (max-width: 600px) {
            .invoice-box table tr.top table td {
                width: 100%;
                display: block;
                text-align: center;
            }
            
            .invoice-box table tr.information table td {
                width: 100%;
                display: block;
                text-align: center;
            }
        }
        
        /** RTL **/
        .rtl {
            direction: rtl;
            font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        }
        
        .rtl table {
            text-align: right;
        }
        
        .rtl table tr td:nth-child(2) {
            text-align: left;
        }''', font_config=font_config)

    pdf_name = str(request.user.id) + "_" + str(time.time())

    html.write_pdf(
        f'/tmp/{pdf_name}.pdf', stylesheets=[css],
        font_config=font_config)

    print(f'/tmp/{pdf_name}.pdf')

    # Send email

    msg = EmailMessage()
    msg['Subject'] = 'Our family reunion'
    msg['From'] = "example@python.sinella.net"
    msg['To'] = str(request.user.email)

    with open(f'/tmp/{pdf_name}.pdf', 'rb') as fp:
        img_data = fp.read()
        msg.add_attachment(img_data, maintype='file', subtype='pdf')

    with smtplib.SMTP(os.environ["SMTP_SERVER"], os.environ["SMTP_PORT"]) as server:
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        server.send_message(msg)

    return True