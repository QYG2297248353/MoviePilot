from fastapi import APIRouter, Depends
from app import schemas
from app.core.security import get_user_id
from app.db.models.sysconfig import SysConfig
from sqlalchemy.orm import Session
from app.db import get_db

router = APIRouter()


@router.get("/dashboard", summary="Get dashboard config", response_model=schemas.SysConfigBase)
def get_dashboard_config(db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    """
    获取仪表盘配置
    找不到用户配置时，返回默认配置
    return: default_dashboard_config
    """
    user_config = SysConfig.get_by_uid(db, user_id)
    if user_config:
        return schemas.SysConfigBase(**user_config.__dict__)
    else:
        SysConfig(uid=user_id).create()
    return schemas.SysConfigBase()


@router.put("/dashboard", summary="Update dashboard config", response_model=schemas.SysConfigBase)
def update_dashboard_config(config: schemas.SysConfigBase, db: Session = Depends(get_db),
                            user_id: int = Depends(get_user_id)):
    """
    更新仪表盘配置
    """
    user_config = SysConfig.get_by_uid(db, user_id)
    if user_config:
        SysConfig.update_by_uid(user_config, db, user_id, **config.dict())
        return config
    else:
        SysConfig(uid=user_id, **config.dict()).create(db)
    return config

# Todo: 删除用户时，删除用户配置
