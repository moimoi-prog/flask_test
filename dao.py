# ①必要なモジュールをインポート
import sqlalchemy.ext.declarative
import sqlalchemy.orm


# クラス
class Dao(object):
    # メタクラスの生成
    Base = sqlalchemy.ext.declarative.declarative_base()

    # テーブル: Task用クラス
    class Tasks(Base):
        __tablename__ = "tasks"
        id = sqlalchemy.Column(
            sqlalchemy.Integer, primary_key=True, autoincrement=True
        )

        name = sqlalchemy.Column(
            sqlalchemy.String(30)
        )

    # コンストラクタ
    def __init__(self):
        # エンジンの生成
        self.engine = sqlalchemy.create_engine("mysql+pymysql://root:@127.0.0.1/example_db")

        # # メタクラスの生成
        # self.Base = sqlalchemy.ext.declarative.declarative_base()

        # 定義したテーブル情報をDBと紐付ける(紐づくテーブルがない場合、生成される。)
        self.Base.metadata.create_all(self.engine)

        Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = Session()

    # レコード一覧を取得する
    def get(self):
        return self.session.query(self.Tasks).all()

    def add(self, name):
        task = self.Tasks(name=name)
        self.session.add(task)
        self.session.commit()

    def delete(self, task_id):
        task = self.session.query(self.Tasks).filter_by(id=task_id).first()
        self.session.delete(task)
        self.session.commit()


