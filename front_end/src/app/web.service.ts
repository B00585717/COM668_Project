import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import { tap } from 'rxjs/operators';

@Injectable()
export class WebService {

  private partyId: any;
  private candidateId: any;
  private voterId: any;

constructor(private http: HttpClient) {}

  getParties(){
    return this.http.get('http://localhost:5000/api/v1.0/parties');
  }

  getParty(p_id: any){
    this.partyId = p_id
    return this.http.get('http://localhost:5000/api/v1.0/parties/' + this.partyId);
  }

  getCandidates(){
    return this.http.get('http://localhost:5000/api/v1.0/candidates');
  }

  getCandidate(c_id: any){
    this.candidateId = c_id
    return this.http.get('http://localhost:5000/api/v1.0/candidates/' + this.candidateId);
  }

  getProfile(){
    const token = localStorage.getItem('access_token');
    const headers = { Authorization: `Bearer ${token}` };
    return this.http.get('http://localhost:5000/api/v1.0/profile', { headers });
  }

  addParty(party: any){
    let formData = this.partyForm(party);
    return this.http.post('http://localhost:5000/api/v1.0/parties', formData);
  }

  addCandidate(candidate: any){
  let formData = this.candidateForm(candidate);
    return this.http.post('http://localhost:5000/api/v1.0/candidates', formData);
  }

  addVoter(voter: any){
    let formData = this.voterForm(voter);
    return this.http.post('http://localhost:5000/api/v1.0/register', JSON.stringify(voter), {headers: { 'Content-Type': 'application/json' }});
  }

  login(voter: any){
    let formData = this.loginForm(voter);
    return this.http.post('http://localhost:5000/api/v1.0/login', formData).pipe(tap((response: any) => {
        localStorage.setItem('access_token', response.access_token);
      }))
  }

  logout() {
    localStorage.removeItem('access_token');
  }

  updateParty(party: any){
    let formData = this.partyForm(party);
    return this.http.put('http://localhost:5000/api/v1.0/parties/'+ this.partyId, formData);
  }


  updateCandidate(candidate: any){
    let formData = this.candidateForm(candidate);
    return this.http.put('http://localhost:5000/api/v1.0/candidates/'+ this.candidateId, formData);
  }

  updatePassword(g_id: string,email: string, newPassword: string) {
    const formData = new FormData();
    formData.append('password', newPassword);
    formData.append('email', email)
    return this.http.put("http://localhost:5000/api/v1.0/profile/"+ g_id , formData);
  }

  private voterForm(voter: any) {

    let formData = new FormData();
    formData.append("first_name", voter.first_name);
    formData.append("last_name", voter.last_name);
    formData.append("email", voter.email);
    formData.append("password", voter.password);
    formData.append("otp", voter.otp);
    formData.append("postcode", voter.postcode);

    return formData;
  }

  private loginForm(voter: any) {

    let formData = new FormData()
    formData.append("gov_id", voter.gov_id);
    formData.append("password", voter.password)

    return formData;
}

  private candidateForm(candidate: any) {

    let formData = new FormData();
    formData.append("candidate_firstname", candidate.candidate_firstname);
    formData.append("candidate_lastname", candidate.candidate_lastname);
    formData.append("party_id", candidate.party_id);
    formData.append("image", candidate.image);
    formData.append("constituency_id", candidate.constituency_id);
    formData.append("statement", candidate.statement);

    return formData;
  }

   private partyForm(party: any) {

    let formData = new FormData();
    formData.append("party_name", party.party_name);
    formData.append("image", party.image);
    formData.append("manifesto", party.manifesto);

    return formData;
  }
}
