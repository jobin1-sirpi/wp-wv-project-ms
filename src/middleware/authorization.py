from typing import Optional
from sqlalchemy.orm import Session
from fastapi.security import OAuth2
from starlette.requests import Request
from fastapi import HTTPException, status, Depends
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param

from ..database.connect import redis_client, get_db
from ..schemas.responses import CustomHttpException
from ..schemas.default_schemas import AuthorizationData


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str = "/auth/login",
        scheme_name: str = "bearer cookie",
        scopes: dict = None,
        description: str = "OAuth2 Password Grant Cookie",
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}

        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})

        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(
        self,
        request: Request,
        db: Session = Depends(get_db),
    ) -> HTTPException | AuthorizationData:
        try:
            authorization_access_token = request.cookies.get("wv_v2_access_token")
            authorization_email = request.cookies.get("wv_v2_email")

            if not authorization_access_token or not authorization_email:
                if self.auto_error:
                    raise CustomHttpException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        message="Unauthorized",
                        error_code="UNAUTHORIZED",
                        error_details="Authentication required. Please login.",
                    )

            scheme, access_token = get_authorization_scheme_param(
                authorization_access_token
            )

            if not access_token or scheme.lower() != "bearer":
                if self.auto_error:
                    raise CustomHttpException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        message="Unauthorized",
                        error_code="UNAUTHORIZED",
                        error_details="Invalid token.",
                    )

            try:
                redis_email = redis_client.get(access_token).decode("utf8")

                if redis_email != authorization_email:
                    if self.auto_error:
                        raise CustomHttpException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            message="Forbidden",
                            error_code="FORBIDDEN",
                            error_details="Token does not belong to the requesting user.",
                        )
            except Exception as e:
                print("Error in OAuth2PasswordBearerHeader middleware:", e)
                if self.auto_error:
                    raise CustomHttpException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        message="Unauthorized",
                        error_code="UNAUTHORIZED",
                        error_details="Token expired.",
                    )

            return {"access_token": access_token, "email": authorization_email}
        except CustomHttpException as e:
            print("Error in OAuth2PasswordBearerHeader middleware:", e)
            raise e
        except Exception as e:
            print("Error in OAuth2PasswordBearerHeader middleware:", e)
            raise CustomHttpException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal Server Error",
                error_code="INTERNAL_SERVER_ERROR",
                error_details="Something went wrong. Please contact developers if issue persists.",
            )
        finally:
            db.close()


oauth2_scheme = OAuth2PasswordBearerCookie()
