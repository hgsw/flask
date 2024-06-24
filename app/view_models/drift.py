from app.libs.enums import PendingStatus


class DriftCollection:
    def __init__(self, drifts, uid):
        self.data = []
        self.__parse(drifts, uid)

    def __parse(self, drifts, uid):
        for drift in drifts:
            temp = DriftViewModel(drift, uid)
            self.data.append(temp.data)


class DriftViewModel:
    def __init__(self, drift, uid):
        self.data = {}

        self.data = self.__parse(drift, uid)

    @staticmethod
    def requester_or_gifter(drift, current_uid):
        you_are = "gifter"
        if drift.requester_id == current_uid:
            you_are = "requester"
        return you_are

    def __parse(self, drift, uid):
        you_are = self.requester_or_gifter(drift, uid)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            "drift_id": drift.id,
            "you_are": you_are,
            # 'book_title': drift.gift.book.title,
            # 'book_author': drift.gift.book.author_str,
            "book_title": drift.book_title,
            "book_author": drift.book_author,
            "book_img": drift.book_img,
            "operator": drift.requester_nickname if you_are != "requester" else drift.gifter_nickname,
            "date": drift.create_datetime.strftime("%Y-%m-%d"),
            "message": drift.message,
            "address": drift.address,
            "recipient_name": drift.recipient_name,
            "mobile": drift.mobile,
            "status_str": pending_status,
            "status": drift.pending,
        }
        return r
