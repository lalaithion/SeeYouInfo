use super::schema::*;
use diesel::pg::data_types::{PgTime};

#[derive(Queryable)]
pub struct Constant {
  // pub id: i32,
  pub value: String,
}

#[derive(Queryable)]
pub struct Class {
    pub id: i32,
    pub code: String,
    pub full_name: String,
    pub description: Option<String>,
}

#[derive(Queryable)]
pub struct Instructor {
    pub id: i32,
    pub full_name: String,
}

#[derive(Queryable)]
pub struct SectionType {
    pub id: i32,
    pub type_: String,
    pub code: String,
}

#[derive(Queryable)]
pub struct Institution {
    pub id: i32,
    pub name: String,
    pub code: String,
}

#[derive(Queryable)]
pub struct InstructionMode {
    pub id: i32,
    pub mode: String,
    pub code: String,
}

#[derive(Insertable, AsChangeset)]
#[table_name="semesters"]
pub struct NewSemester<'a> { 
  // pub id: i32,
  pub year: i32,
  pub season: &'a str,
}

#[derive(Insertable, AsChangeset)]
#[table_name="section_types"]
pub struct NewSectionType<'a> { 
  // pub id: i32,
  pub type_: &'a str,
}

#[derive(Insertable, AsChangeset)]
#[table_name="classes"]
pub struct NewClass<'a> {
  // pub id: i32,
  pub code: &'a str,
  pub full_name: &'a str,
  pub description: &'a str,
}

#[derive(Insertable, AsChangeset)]
#[table_name="instructors"]
pub struct NewInstructor {
  // pub id: i32,
  pub full_name: String,
}

#[derive(Insertable, AsChangeset, Debug)]
#[table_name="sections"]
pub struct NewSection<'a> {
  pub crn: i32,
  pub section_no: &'a str,
  pub parent_class: i32, // REFERENCES classes
  pub section_type: i32, // REFERENCES section_types
  pub institution: i32, // REFERENCES institutions
  pub mode: i32, // REFERENCES instruction_modes

  pub semester: i32, // REFERENCES semesters
  pub start_time: Option<PgTime>,
  pub end_time: Option<PgTime>,
  
  pub monday: bool,
  pub tuesday: bool,
  pub wednesday: bool,
  pub thursday: bool,
  pub friday: bool,
  pub saturday: bool,
  pub sunday: bool,

  pub instructor: Vec<i32>, // REFERENCES instructors
  pub credits: f32,
  pub total_seats: i32,
  pub available_seats: i32,
  pub waitlist: i32,

  pub is_cancelled: bool,
  pub special_date_range: bool,
  pub no_auto_enroll: bool,
  // pub section_name: &'a str,
}