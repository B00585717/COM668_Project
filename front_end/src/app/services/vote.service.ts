import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {AuthService} from "./auth.service";

@Injectable({
  providedIn: 'root'
})
export class VoteService {

  constructor(private http: HttpClient,
              private authService: AuthService) { }

  voteForCandidate(voter_id: number, candidate_id: number, vote_type: number) {
    const headers = new HttpHeaders().set('Authorization', 'Bearer ' + this.authService.getToken());
    return this.http.post('http://localhost:5000/api/v1.0/votes', { voter_id, candidate_id, vote_type }, { headers });
  }

  getRemainingVotes(voter_id: string) {
    const headers = new HttpHeaders().set('Authorization', 'Bearer ' + this.authService.getToken());
    return this.http.get<{remaining_positive_votes: number, remaining_negative_votes: number}>('http://localhost:5000/api/v1.0/remaining-votes/'+ voter_id, { headers });
  }
}



