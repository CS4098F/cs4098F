process Dementia_management {

  action identify_causal_or_exacerbating_factors { 
    requires { Guidelines_For_Treatment_Of_Patients }
  }
  action provide_patient_carer_with_information {
    agent {GP && patient && carer}
    requires {
      patient_record.Confirmed_Dementia
      && patient_record.requests_privacy == "false" 
    }
    provides { information_to_carer }
  }	
  action create_treatment_or_care_plan {
    agent {
      memory_assessment_service 
      && GP && clinical_psychologiest && nurses
      && occupational_therapists && phsiotherapists 
      && speech_and_language_therapists 
      && social_workers && voluntary_organisation
    }
    requires { patient_history }
    provides { care_plan }
  }
  action formal_review_of_care_plan {
    agent { person && carer }
    requires { care_plan }
    provides { care_plan.reviewed == "true" } 
  }
  action assess_carer_needs { 
    agent { carer}
    provides { care_plan.respite_care }
  }
}


