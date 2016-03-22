# -*- coding: utf-8 -*-
"""
All channels for the stream
"""
from __future__ import absolute_import

from flask import session, current_app
from flask_socketio import SocketIO, emit, disconnect, close_room, rooms, leave_room, join_room


STARTING_COUNT = 0


def create_stream(app, **kwargs):
    """
    Create a new Socket.io Stream attached to all common channels

    :param app: Flask application to register against
    :return: SocketIO instance with all common listeners attached
    """
    stream = SocketIO(app, **kwargs)
    _add_channels(stream)
    return stream


def increment_message_number():
    """
    Maintain a unique count of messages received for this session.

    This allows custom variables to be tracked on a per user basis.

    :return: Next count value
    """
    count = session.get('receive_count', STARTING_COUNT) + 1
    session['receive_count'] = count
    return count


def _add_channels(stream):
    """
    Add all routes to the stream

    :param stream: Stream listeners
    :return:
    """
    ####################################################################################################
    # SYSTEM
    ####################################################################################################
    @stream.on('connect')
    def test_connect():
        count = increment_message_number()
        emit('receive system', {'data': 'Connected', 'count': count})

    @stream.on('disconnect')
    def test_disconnect():
        """
        Disconnected.  Can't emit here.
        """

    @stream.on('disconnect request')
    def disconnect_request():
        print 'here'
        count = increment_message_number()
        emit('receive system', {'data': 'Disconnected!', 'count': count})
        disconnect()

    ####################################################################################################
    # ECHO
    ####################################################################################################
    @stream.on('echo')
    def test_message(message):
        count = increment_message_number()
        data = message['data']
        emit('receive echo', {'data': data, 'count': count})

    @stream.on('broadcast')
    def test_broadcast_message(message):
        count = increment_message_number()
        data = message['data']
        emit('receive broadcast', {'data': data, 'count': count}, broadcast=True)

    ####################################################################################################
    # ROOMS
    ####################################################################################################
    @stream.on('join room')
    def join(message):
        join_room(message['room'])
        list_of_rooms = ', '.join(rooms())
        emit('receive room', {'data': list_of_rooms})

    @stream.on('leave room')
    def leave(message):
        leave_room(message['room'])
        list_of_rooms = ', '.join(rooms())
        emit('receive room', {'data': list_of_rooms})

    @stream.on('close room')
    def close(message):
        room = message['room']
        data = room + ' closing.'
        emit('receive room', {'data': data}, room=room)
        close_room(room)

    @stream.on('broadcast room')
    def send_room_message(message):
        room = message['room']
        data = message['data']
        user = message['user']
        emit('receive room broadcast', {'data': data, 'room': room, 'user': user}, room=room)


    ####################################################################################################
    # ERRORS
    ####################################################################################################
    @stream.on_error()
    def error_handler(e):
        current_app.logger.exception('Ruh roh!  %s', e)
