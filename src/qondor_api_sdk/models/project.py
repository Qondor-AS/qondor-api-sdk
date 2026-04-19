from __future__ import annotations

from .._base import ApiModel
from .enums import CustomFieldDataType, ISO4217CurrencyCode, ProjectStatus

__all__ = [
    "ProjectCustomFieldAnswerIn",
    "SetAsFinished",
    "CreateProject",
    "ProjectCustomFieldAnswerDetails",
    "ProjectDetails",
    "ProjectManagerDetails",
    "ProjectSummary",
]


class ProjectCustomFieldAnswerIn(ApiModel):
    id: int | None = None
    external_reference: str | None = None
    answer: str | None = None


class SetAsFinished(ApiModel):
    project_id: int | None = None
    project_no: str | None = None
    office_id: int | None = None
    real_sales: float | None = None
    real_revenue: float | None = None


class CreateProject(ApiModel):
    office_id: int | None = None
    name: str | None = None
    project_no: str | None = None
    copy_from_project_no: str | None = None
    main_project_manager_id: int | None = None
    main_project_manager_user_name: str | None = None
    customer_id: int | None = None
    customer_external_reference: str | None = None
    customer_number: str | None = None
    main_contact_person_id: int | None = None
    main_contact_person_email: str | None = None
    main_contact_person_external_reference: str | None = None
    team_id: int | None = None
    team_external_reference: str | None = None
    pax: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    location_code: str | None = None
    location: str | None = None
    budgeted_sales: float | None = None
    budgeted_revenue: float | None = None
    currency: str | None = None
    lead_from: str | None = None
    project_category: str | None = None
    project_custom_field_answers: list[ProjectCustomFieldAnswerIn] | None = None


class ProjectCustomFieldAnswerDetails(ApiModel):
    heading: str | None = None
    answer: str | None = None
    external_reference: str | None = None
    data_type: CustomFieldDataType | None = None
    data_type_text: str | None = None


class ProjectDetails(ApiModel):
    id: int | None = None
    name: str | None = None
    project_no: str | None = None
    is_agent_mode: bool | None = None
    office_id: int | None = None
    office_name: str | None = None
    office_internal_name: str | None = None
    office_external_reference: str | None = None
    office_country_code: str | None = None
    customer_id: int | None = None
    customer_name: str | None = None
    customer_number: str | None = None
    customer_external_reference: str | None = None
    status: ProjectStatus | None = None
    status_text: str | None = None
    destination: str | None = None
    destination_country_code: str | None = None
    location: str | None = None
    location_country_code: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    invoice_copies_to: str | None = None
    customer_number_for_booking_invoicing: str | None = None
    created_date: str | None = None
    confirmation_date: str | None = None
    cancellation_date: str | None = None
    settings_last_edited_date: str | None = None
    first_offer_sent_date: str | None = None
    pax: int | None = None
    project_category_id: int | None = None
    project_category: str | None = None
    lead_from_id: int | None = None
    lead_from: str | None = None
    project_cancellation_reason: str | None = None
    project_cancellation_reason_other_information: str | None = None
    project_leaders: list[ProjectManagerDetails] | None = None
    project_managers: list[ProjectManagerDetails] | None = None
    is_anonymised: bool | None = None
    project_custom_field_answers: list[ProjectCustomFieldAnswerDetails] | None = None
    project_currency_code_deprecated: str | None = None
    currency_code: ISO4217CurrencyCode | None = None
    currency: str | None = None
    team_id: int | None = None
    team_name: str | None = None
    team_external_reference: str | None = None


class ProjectManagerDetails(ApiModel):
    first_name: str | None = None
    last_name: str | None = None
    id: int | None = None
    full_name: str | None = None
    email: str | None = None
    is_main_project_leader: bool | None = None
    is_main_project_manager: bool | None = None
    involvement: int | None = None


class ProjectSummary(ApiModel):
    id: int | None = None
    name: str | None = None
    project_no: str | None = None
    is_agent_mode: bool | None = None
    office_id: int | None = None
    office_name: str | None = None
    office_internal_name: str | None = None
    office_country_code: str | None = None
    customer_id: int | None = None
    customer_name: str | None = None
    customer_number: str | None = None
    status: ProjectStatus | None = None
    status_text: str | None = None
    destination: str | None = None
    destination_country_code: str | None = None
    location: str | None = None
    location_country_code: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    created_date: str | None = None
    confirmation_date: str | None = None
    cancellation_date: str | None = None
    settings_last_edited_date: str | None = None
    first_offer_sent_date: str | None = None
    pax: int | None = None
    project_category_id: int | None = None
    project_category: str | None = None
    lead_from_id: int | None = None
    lead_from: str | None = None
    project_cancellation_reason: str | None = None
    project_cancellation_reason_other_information: str | None = None
    project_leaders: list[ProjectManagerDetails] | None = None
    project_managers: list[ProjectManagerDetails] | None = None
    is_anonymised: bool | None = None
    project_custom_field_answers: list[ProjectCustomFieldAnswerDetails] | None = None
    project_currency_code_deprecated: str | None = None
    currency_code: ISO4217CurrencyCode | None = None
    currency: str | None = None
