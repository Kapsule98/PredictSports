HTTP Method         URL                                         Authentication
GET                 /                                               JWT
POST                /register               
POST                /login
GET                 /logout                                         JWT
POST                /makeprediction                                 JWT
GET                 /getprediction
GET                 /getprediction/username                         JWT
GET                 /getprediction/matchid                          JWT
GET                 /getprediction/username/matchid                 JWT
POST                /user/username              

#### API description
<table>
<tr>
<td>HTTP METHOD</td>
<td>URL</td>
<td>AUTHENTICATION</td>
<td>DESCRIPTION</td>
</tr>
<tr>
<td>GET</td>
<td>/</td>
<td>JWT</td>
<td>Returns Index page info</td>
</tr>
<tr>
<td>POST</td>
<td>/regiser</td>
<td></td>
<td>Register new user</td>
</tr>
<tr>
<td>POST</td>
<td>/login</td>
<td></td>
<td>Login user</td>
</tr>
<tr>
<td>GET</td>
<td>/logout</td>
<td>JWT</td>
<td>User logout</td>
</tr>
<tr>
<td>POST</td>
<td>/makeprediction</td>
<td>JWT</td>
<td>make prediction (send username and matchid in request json)</td>
</tr>
<tr>
<td>GET</td>
<td>/getprediction</td>
<td>JWT</td>
<td>get all predictions</td>
</tr>
<tr>
<td>GET</td>
<td>/getprediction/:username</td>
<td>JWT</td>
<td>get all predictions made by user = username</td>
</tr>
<tr>
<td>GET</td>
<td>/getprediction/:matchid</td>
<td>JWT</td>
<td>get all predictions made for match = matchid</td>
</tr>
<tr>
<td>GET</td>
<td>/getprediction/:username/:matchid</td>
<td>JWT</td>
<td>get prediction made by user = username for match = matchid</td>
</tr>
<tr>
<td>POST</td>
<td>/user/:username</td>
<td>JWT</td>
<td>Update user score</td>
</tr>
</table>