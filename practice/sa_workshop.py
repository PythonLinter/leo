
from nanohttp.contexts import Context
from restfulpy.orm import DBSession, DeclarativeBase
from sqlalchemy import func, select, and_
from sqlalchemy.orm import mapper

from leo import leo
from leo.models import Icd, Collection, collection_icd_table, Member


leo.configure()
leo.initialize_models()


if __name__ == '__main__':
    with Context({}) as context:
        context.identity = vahid = Member.query.filter(Member.email == 'vahid@carrene.com').one()
        # vahid.ensure_builtin_collections()
        # DBSession.commit()
        #
        # favorites = vahid.collections.filter(Collection.title == 'Favorites').one()
        # favorites.codes.append(Icd.query.filter(Icd.id == 1).one())
        # DBSession.commit()

        collections_cte = select([
            Collection.id.label('collection_id'),
            collection_icd_table.c.icd_id.label('icd_id')
        ]).select_from(
            Collection.__table__.join(
                collection_icd_table, collection_icd_table.c.collection_id == Collection.id
            )
        ).where(
            Collection.user_id == context.identity.id
        ).cte()

        q = select([
            Icd.id,
            Icd.code,
            func.array_remove(func.array_agg(collections_cte.c.collection_id), None).label('collections'),
        ]).select_from(
            Icd.__table__.outerjoin(
                collections_cte, Icd.id == collections_cte.c.icd_id
            )
        ).group_by(
            Icd.id,
            Icd.code
        ).alias()


        class IcdView:
            collections = None

        mapper(IcdView, q)

            # __table__ = q
        # for flags, icd, collections in q[:10]:
        #     print(flags, icd.id, collections)

        for i in DBSession.query(IcdView)[:10]:
            print(i.id, i.code, i.collections)

