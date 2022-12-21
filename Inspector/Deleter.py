# coding=utf-8
def deleter_key(delete, c_id):
    for key in delete:
        if key in c_id:
            c_id.pop(key)
    return c_id

def language(m_id, Sheet, id):
    m_id['language'] = Sheet['Access_id_language'][str(id)][-1]
    if 'UA' in m_id['language']:
        m_id['language'] = 0
    elif 'EN' in m_id['language']:
        m_id['language'] = 1
    elif 'TR' in m_id['language']:
        m_id['language'] = 2
    return m_id