from tinyfeedback.helper import tail_monitor

def parse_line(data, line):
    if 'GET / ' in line:
        data['site.hits'] += 1

if __name__ == '__main__':
    global last_count
    tail_monitor(component='istherechickenbroccolibake',
            log_filename='/tmp/itcbb.log',
            line_callback_func=parse_line,
            data_arg={'site.hits': 0, 'sms.received': 0, 'sms.sent': 0},
            )
