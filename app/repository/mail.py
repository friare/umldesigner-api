from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME = "genereuxakotenou@yahoo.fr",
    MAIL_PASSWORD = "dqoxrscrzcrmrkqn",
    MAIL_FROM = "genereuxakotenou@yahoo.fr",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.mail.yahoo.com",
    MAIL_FROM_NAME="UMLDesigner",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

#MAIL D'ACTIVATION DE COMPTE
template_new_account = """
<div style="margin:0;box-sizing:border-box;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;min-width:100%;padding:0;text-align:left;width:100%!important">
    <span style="color:#f3f3f3;display:none!important;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden">UMLDesigner Mail Service</span>
    <table style="margin:0;background:#f3f3f3;border-collapse:collapse;border-spacing:0;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;height:100%;line-height:1.3;margin:0;padding:0;text-align:left;vertical-align:top;width:100%">
       <tbody>
          <tr style="padding:0;text-align:left;vertical-align:top">
             <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" valign="top" align="center">
                <center style="min-width:640px;width:100%">
                   <table style="margin:0 auto;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:100%">
                      <tbody>
                         <tr style="padding:0;text-align:left;vertical-align:top">
                            <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:30px;font-weight:400;line-height:30px;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" height="50px"> 							&nbsp;</td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="margin:0 auto;background:#f3f3f3;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:640px" align="center">
                      <tbody>
                         <tr style="padding:0;text-align:left;vertical-align:top">
                            <td style="text-align:center;margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0;vertical-align:top;word-wrap:break-word"> 							 						</td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="margin:0 auto;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:100%">
                      <tbody>
                         <tr style="padding:0;text-align:left;vertical-align:top">
                            <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:30px;font-weight:400;line-height:30px;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" height="50px"> 							&nbsp;</td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="border-radius:4px;margin:0 auto;background:#fff;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:640px;border-top:7px solid #6c63ff;display:block" align="center">
                      <tbody>
                         <tr style="border-spacing:0;float:none;padding:0;text-align:left;vertical-align:top">
                            <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word">
                               <table style="border-collapse:collapse;border-spacing:0;display:table;padding:0;text-align:left;vertical-align:top;width:100%">
                                  <tbody>
                                     <tr style="border-spacing:0;float:none;padding:0;text-align:left;vertical-align:top">
                                        <th style="margin:0 auto;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0 auto;padding-bottom:0px;padding-left:30px;padding-right:30px;padding-top:30px;text-align:left;width:610px">
                                           <table style="border-collapse:collapse;border-spacing:0;padding:0;text-align:left;vertical-align:top;width:100%">
                                              <tbody>
                                                 <tr style="border-spacing:0;float:none;padding:0;text-align:left;vertical-align:top">
                                                    <th style="margin:0;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0;text-align:left">
                                                       <p style="text-align:center;padding-bottom:20px">
                                                       <img width="100" src="https://raw.githubusercontent.com/Genereux-akotenou/mess-files/37c7d9c3def2be30ef46a96bcc9a580305dd1118/umld.svg" alt="lock icon" class="CToWUd"></p>
                                                       <p style="margin:0;text-align:center;font-size:18px;color:#666">  	Bienvenu sur UMLDESIGNER</p>
                                                       <!--<p style="margin:10px auto 0px auto;text-align:center;font-size:14px;color:#666;line-height:20px">Votre application de conception UML par description textuelle.</p>-->
                                                       <p style="margin:0;text-align:center;font-size:20px;color:#6c63ff">  	<strong><a style="color:#6c63ff" href="mailto:{}" target="_blank">{}</a></strong></p>
                                                       <p style="text-align:center">  	&nbsp;</p>
                                                       <p style="text-align:center;font-size:14px;color:#666">  	Il ne reste plus qu'une chose à faire pour activer votre compte et retrouver l'accès à votre espace de travail umlDesigner</p>
                                                       <p style="margin:0 auto;text-align:center;font-size:14px;color:#666"></p>
                                                       <p style="margin:20px 0px 50px 0px;text-align:center">
                                                            <a style="background-color:#6c63ff;border-radius:3px;color:#fff;display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:14px;margin:0 auto;padding:10px 16px;text-decoration:none" href="{}" target="_blank">
                                                                ACTIVER MON COMPTE
                                                            </a>
                                                        </p>
                                                        <p style="margin:0 auto;text-align:center;font-size:14px;color:#666">  	Si vous n'avez pas créer de compte sur <a href="https://umldesigner.app" target="_blank">umldesigner.app</a>, veuillez ignorer ce message. La sécurité de votre mot de passe n'a pas été compromise.</p>
                                                       <p style="text-align:center;margin:0">  	&nbsp;</p>
                                                       <p style="text-align:center;margin:0">  	&nbsp;</p>
                                                       <p style="text-align:center;margin:0">  	&nbsp;</p>
                                                       <p style="margin:40px auto 0px auto;text-align:center;font-size:14px;color:#666;line-height:20px">Cordiallement, <strong>&nbsp;UMLDesigner</strong></p>
                                                    </th>
                                                    <th style="margin:0;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0!important;text-align:left;width:0"></th>
                                                 </tr>
                                              </tbody>
                                           </table>
                                        </th>
                                     </tr>
                                  </tbody>
                               </table>
                               <table style="border-collapse:collapse;border-spacing:0;padding:0;text-align:left;vertical-align:top;width:100%">
                                  <tbody>
                                     <tr style="padding:0;text-align:left;vertical-align:top">
                                        <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:30px;font-weight:400;line-height:30px;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" height="30px"> 										&nbsp;</td>
                                     </tr>
                                  </tbody>
                               </table>
                            </td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="margin:0 auto;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:100%">
                      <tbody>
                         <tr style="padding:0;text-align:left;vertical-align:top">
                            <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:30px;font-weight:400;line-height:30px;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" height="30px"> 							&nbsp;</td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="margin:0 auto;background:#f3f3f3;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:640px" align="center">
                      <tbody>
                         <tr style="padding:0;vertical-align:top;padding-bottom:1em;">
                            <td style="margin-bottom: 2em !important;"><span style="margin:0;border-collapse:collapse!important;color:#777777;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;margin:0;padding:0;text-align:center;vertical-align:text-bottom;word-wrap:break-word">Powered by</span> &nbsp;<span style="color:#6c63ff;font-family:'Arial Black';font-size:18px;letter-spacing:-0.24px">UMLDESIGNER</span> 			<br><br>			</td>
                         </tr>
                      </tbody>
                   </table>
                </center>
             </td>
          </tr>
       </tbody>
    </table>
    <div class="yj6qo"></div>
    <div class="adL"> </div>
    <div style="display:none;white-space:nowrap;font:15px courier;line-height:0" class="adL">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 	&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 	&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>
    <div class="adL"> </div>
 </div>
"""

invitation_to_project = """\
<div style="margin:0;box-sizing:border-box;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;min-width:100%;padding:0;text-align:left;width:100%!important">
    <span style="color:#f3f3f3;display:none!important;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden">UMLdesigner Mail Service</span>
    <table style="margin:0;background:#f3f3f3;border-collapse:collapse;border-spacing:0;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;height:100%;line-height:1.3;margin:0;padding:0;text-align:left;vertical-align:top;width:100%">
       <tbody>
          <tr style="padding:0;text-align:left;vertical-align:top">
             <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" valign="top" align="center">
                <center style="min-width:640px;width:100%">
                   <table style="margin:0 auto;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:100%">
                      <tbody>
                         <tr style="padding:0;text-align:left;vertical-align:top">
                            <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:30px;font-weight:400;line-height:30px;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" height="50px"> 							&nbsp;</td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="margin:0 auto;background:#f3f3f3;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:640px" align="center">
                      <tbody>
                         <tr style="padding:0;text-align:left;vertical-align:top">
                            <td style="text-align:center;margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0;vertical-align:top;word-wrap:break-word"> 							 						</td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="margin:0 auto;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:100%">
                      <tbody>
                         <tr style="padding:0;text-align:left;vertical-align:top">
                            <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:30px;font-weight:400;line-height:30px;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" height="50px"> 							&nbsp;</td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="border-radius:4px;margin:0 auto;background:#fff;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:640px;border-top:7px solid #6c63ff;display:block" align="center">
                      <tbody>
                         <tr style="border-spacing:0;float:none;padding:0;text-align:left;vertical-align:top">
                            <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word">
                               <table style="border-collapse:collapse;border-spacing:0;display:table;padding:0;text-align:left;vertical-align:top;width:100%">
                                  <tbody>
                                     <tr style="border-spacing:0;float:none;padding:0;text-align:left;vertical-align:top">
                                        <th style="margin:0 auto;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0 auto;padding-bottom:0px;padding-left:30px;padding-right:30px;padding-top:30px;text-align:left;width:610px">
                                           <table style="border-collapse:collapse;border-spacing:0;padding:0;text-align:left;vertical-align:top;width:100%">
                                              <tbody>
                                                 <tr style="border-spacing:0;float:none;padding:0;text-align:left;vertical-align:top">
                                                    <th style="margin:0;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0;text-align:left">
                                                       <p style="text-align:center;padding-bottom:20px">
                                                       <img width="100" src="https://raw.githubusercontent.com/Genereux-akotenou/mess-files/37c7d9c3def2be30ef46a96bcc9a580305dd1118/umld.svg" alt="lock icon" class="CToWUd"></p>
                                                       <p style="margin:0;text-align:center;font-size:18px;color:#666">  	UMLDESIGNER</p>
                                                       <!--<p style="margin:10px auto 0px auto;text-align:center;font-size:14px;color:#666;line-height:20px">Votre application de conception UML par description textuelle.</p>-->
                                                       <p style="margin:0;text-align:center;font-size:20px;color:#6c63ff"></p>
                                                       <p style="text-align:center">  	&nbsp;</p>
                                                       <p style="text-align:center;font-size:14px;color:#666">  	Hi. Vous avez été invitez par <strong>{}</strong> à rejoindre le projet de conception de diagramme UML intitulé <strong>{}</strong>. Vous êtes totallement libre d'accepter ou de rejeter cette invitation. </p>
                                                       <p style="margin:0 auto;text-align:center;font-size:14px;color:#666"></p>
                                                       <p style="margin:20px 0px 50px 0px;text-align:center">
                                                            <a style="background-color:#e53f4b;border-radius:3px;color:#fff;display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:14px;margin:0 auto;padding:10px 16px;text-decoration:none" href="{}" target="_blank">
                                                                REJETER
                                                            </a>
                                                            <a style="background-color:#6c63ff;border-radius:3px;color:#fff;display:inline-block;font-family:Helvetica,Arial,sans-serif;font-size:14px;margin:0 auto;padding:10px 16px;text-decoration:none" href="{}" target="_blank">
                                                                ACCEPTER L'INVITATION
                                                            </a>
                                                        </p>
                                                        <p style="margin:0 auto;text-align:center;font-size:14px;color:#666">  	NB: Si vous n'avez pas encore de compte sur <a href="https://umldesigner.app" target="_blank">umldesigner.app</a>, en cliquantsur "accepter" vous serai amener a créer un compte avant d'être affecter a votre projet. Veuillez donc lire et accepter nos termes et politiques.</p>
                                                       <p style="text-align:center;margin:0">  	&nbsp;</p>
                                                       <p style="text-align:center;margin:0">  	&nbsp;</p>
                                                       <p style="text-align:center;margin:0">  	&nbsp;</p>
                                                       <p style="margin:40px auto 0px auto;text-align:center;font-size:14px;color:#666;line-height:20px">Cordiallement, <strong>&nbsp;UMLDesigner</strong></p>
                                                    </th>
                                                    <th style="margin:0;color:#505050;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;line-height:1.3;margin:0;padding:0!important;text-align:left;width:0"></th>
                                                 </tr>
                                              </tbody>
                                           </table>
                                        </th>
                                     </tr>
                                  </tbody>
                               </table>
                               <table style="border-collapse:collapse;border-spacing:0;padding:0;text-align:left;vertical-align:top;width:100%">
                                  <tbody>
                                     <tr style="padding:0;text-align:left;vertical-align:top">
                                        <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:30px;font-weight:400;line-height:30px;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" height="30px"> 										&nbsp;</td>
                                     </tr>
                                  </tbody>
                               </table>
                            </td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="margin:0 auto;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:100%">
                      <tbody>
                         <tr style="padding:0;text-align:left;vertical-align:top">
                            <td style="margin:0;border-collapse:collapse!important;color:#505050;font-family:Roboto,sans-serif;font-size:30px;font-weight:400;line-height:30px;margin:0;padding:0;text-align:left;vertical-align:top;word-wrap:break-word" height="30px"> 							&nbsp;</td>
                         </tr>
                      </tbody>
                   </table>
                   <table style="margin:0 auto;background:#f3f3f3;border-collapse:collapse;border-spacing:0;float:none;margin:0 auto;padding:0;text-align:center;vertical-align:top;width:640px" align="center">
                      <tbody>
                         <tr style="padding:0;vertical-align:top;padding-bottom:1em;">
                            <td style="margin-bottom: 2em !important;"><span style="margin:0;border-collapse:collapse!important;color:#777777;font-family:Roboto,sans-serif;font-size:14px;font-weight:400;margin:0;padding:0;text-align:center;vertical-align:text-bottom;word-wrap:break-word">Powered by</span> &nbsp;<span style="color:#6c63ff;font-family:'Arial Black';font-size:18px;letter-spacing:-0.24px">UMLDESIGNER</span> 			<br><br>			</td>
                         </tr>

                      </tbody>
                   </table>
                </center>
             </td>
          </tr>
       </tbody>
    </table>
    <div class="yj6qo"></div>
    <div class="adL"> </div>
    <div style="display:none;white-space:nowrap;font:15px courier;line-height:0" class="adL">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 	&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 	&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div>
    <div class="adL"> </div>
 </div>
"""