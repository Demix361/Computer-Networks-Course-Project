import select, socket, sys
from protocol import MyProtocol

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(('', 9090))
server.listen(4)
socket_list = [server]
clients = []
positions = []
animations = []
max_clients = 3

while socket_list:
    sockets_to_read, _, _ = select.select(socket_list, [], [])
    for s in sockets_to_read:
        if s is server:
            print('here 0')
            connection, client_address = s.accept()
            connection.setblocking(0)
            socket_list.append(connection)
        else:
            if s not in clients:
                clients.append(s)
                positions.append([0, 0])
                animations.append('none')
            data = s.recv(10000)
            if data:
                # Обработка сообщений
                mes = MyProtocol.getDataFromByteStr(data)
                if mes['type'] == 'connect':
                    #print('clients: ', clients)
                    player_id = len(clients)
                    answer = {'type': 'connected', 'player_id': player_id}
                    answer_bit = MyProtocol.getByteStrFromData(answer)
                    s.send(answer_bit)
                elif mes['type'] == 'ask':
                    if mes['question'] == 'players_connected':
                        answer = {'type': 'ask', 'players_connected': len(clients)}
                        answer_bit = MyProtocol.getByteStrFromData(answer)
                        s.send(answer_bit)
                    if mes['question'] == 'game_ready':
                        answer = {'type': 'ask', 'question': 'game_ready'}
                        if len(clients) == max_clients:
                            answer['answer'] = 'yes'
                        else:
                            answer['answer'] = 'no'
                        answer_bit = MyProtocol.getByteStrFromData(answer)
                        s.send(answer_bit)
                elif mes['type'] == 'start':
                    answer = {'type': 'start'}
                    answer_bit = MyProtocol.getByteStrFromData(answer)
                    for client in clients:
                        client.send(answer_bit)
                elif mes['type'] == 'position':
                    positions[mes['player_id'] - 1] = mes['pos']
                    animations[mes['player_id'] - 1] = mes['anim']

                    answer = {'type': 'position'}
                    for i in range(len(clients)):
                        if i != mes['player_id'] - 1:
                            answer[f'pos_{i + 1}'] = positions[i]
                            answer[f'anim_{i + 1}'] = animations[i]

                    #for e in mes['enemy_info']:


                    answer_bit = MyProtocol.getByteStrFromData(answer)
                    s.send(answer_bit)


            # else:
            #     print('here 3')
            #     socket_list.remove(s)
            #     s.close()
